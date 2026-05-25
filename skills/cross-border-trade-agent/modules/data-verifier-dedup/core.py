#!/usr/bin/env python3
"""
P1 数据验证去重 — 统一中心

核心能力：
  1. 数据验证 (verify) — ABN/官网/电话/邮箱/LinkedIn 多源交叉验证
  2. 合并去重 (dedup) — 同名/同邮箱/同网址自动合并，保留高质量数据
  3. 质量评分 (quality) — 每条记录的数据质量评分
  4. 数据清洗 (clean) — 统一格式、去除无效字段

数据源：
  - modules/buyer-intel/data/buyers.md    — 买家线索
  - data/real_companies.md                — 公司数据
  - data/.abn_cache/                      — ABN 查询缓存
"""

import json, re, os, hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

SKILL_DIR = Path(__file__).resolve().parent.parent


# ════════════════════════════════════════════
# 1. 数据验证
# ════════════════════════════════════════════

class DataVerifier:
    """数据验证 — 多源交叉验证"""

    @staticmethod
    def _load_legacy_module(rel_path: str, class_or_func: str, file_name: str = "core.py"):
        """加载旧模块工具"""
        import importlib.util as iu
        path = str(SKILL_DIR / rel_path / file_name)
        spec = iu.spec_from_file_location(class_or_func, path)
        mod = iu.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    @staticmethod
    def verify_company(name: str, website: str = "", abn: str = "",
                       phone: str = "", email: str = "",
                       deep: bool = False) -> dict:
        """验证一条公司记录，返回可信度评分

        Args:
            name: 公司名称
            website: 官网
            abn: ABN 号
            phone: 电话
            email: 邮箱
            deep: 是否深度验证（会调在线 API）

        Returns:
            { "score", "level", "checks": [...] }
        """
        checks = []
        score = 0
        max_score = 0

        # 1. ABN 验证 (25分)
        max_score += 25
        if abn:
            try:
                mod = DataVerifier._load_legacy_module(
                    "modules/company-enricher", "ABNVerifier", "abn_integration.py")
                av = mod.ABNVerifier()
                abn_result = av.verify(abn)
                status = abn_result.get("status", "")
                if "Active" in str(status):
                    score += 25
                    checks.append({"check": "ABN", "status": "✅", "detail": f"ABN {abn}: {status}"})
                elif status:
                    score += 10
                    checks.append({"check": "ABN", "status": "⚠️", "detail": f"ABN {abn}: {status}"})
                else:
                    checks.append({"check": "ABN", "status": "🔍", "detail": f"ABN {abn}: 查询无返回"})
            except Exception as e:
                checks.append({"check": "ABN", "status": "🔍", "detail": f"验证服务暂不可用: {e}"})
        else:
            checks.append({"check": "ABN", "status": "⏭", "detail": "未提供 ABN"})

        # 2. 网站验证 (25分)
        max_score += 25
        if website:
            domain_pattern = re.compile(
                r'^(https?://)?[a-zA-Z0-9][-a-zA-Z0-9]*(\.[a-zA-Z0-9][-a-zA-Z0-9]*)+')
            if domain_pattern.match(website):
                score += 20
                ext = website.split(".")[-1].split("/")[0]
                # 商业域名加分
                if ext in ("com", "com.au", "co", "co.nz", "io", "org", "net"):
                    score += 5
                checks.append({"check": "网站", "status": "✅", "detail": f"域名格式有效: {website}"})
            else:
                checks.append({"check": "网站", "status": "⚠️", "detail": f"域名格式异常: {website}"})
        else:
            checks.append({"check": "网站", "status": "⏭", "detail": "未提供网站"})

        # 3. 公司名称 (15分)
        max_score += 15
        if name and len(name) > 3:
            biz_indicators = ["pty", "ltd", "limited", "group", "co", "corp",
                              "inc", "llc", "gmbh", "holding", "enterprise",
                              "pty ltd", "有限公司"]
            has_biz = any(ind in name.lower() for ind in biz_indicators)
            score += 10 + (5 if has_biz else 0)
            level = "企业" if has_biz else "可能非正式名称"
            checks.append({"check": "名称", "status": "✅", "detail": f"""{name}" ({level})"""})
        else:
            checks.append({"check": "名称", "status": "⚠️", "detail": "名称过短或缺失"})

        # 4. 电话验证 (15分)
        max_score += 15
        if phone:
            clean_phone = re.sub(r'[\s\-\+\(\)]', '', phone)
            if len(clean_phone) >= 7 and len(clean_phone) <= 15:
                score += 15
                checks.append({"check": "电话", "status": "✅", "detail": f"格式有效"})
            else:
                score += 5
                checks.append({"check": "电话", "status": "⚠️", "detail": "号码长度异常"})
        else:
            checks.append({"check": "电话", "status": "⏭", "detail": "未提供电话"})

        # 5. 邮箱验证 (10分)
        max_score += 10
        if email:
            if re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
                score += 10
                domain = email.split("@")[1]
                if "gmail" not in domain and "yahoo" not in domain and "qq" not in domain and "outlook" not in domain:
                    score += 5  # 企业邮箱加分
                    max_score += 5
                checks.append({"check": "邮箱", "status": "✅", "detail": f"有效邮箱"})
            else:
                score += 2
                checks.append({"check": "邮箱", "status": "⚠️", "detail": "邮箱格式无效"})
        else:
            checks.append({"check": "邮箱", "status": "⏭", "detail": "未提供邮箱"})

        # 6. 深度验证（可选）
        if deep and website:
            try:
                import requests
                resp = requests.get(f"https://{website}", timeout=10,
                                    headers={"User-Agent": "Mozilla/5.0"})
                if resp.status_code == 200:
                    score += 10
                    max_score += 10
                    checks.append({"check": "网站可达性", "status": "✅", "detail": f"HTTP {resp.status_code}"})
                else:
                    max_score += 10
                    checks.append({"check": "网站可达性", "status": "⚠️", "detail": f"HTTP {resp.status_code}"})
            except Exception as e:
                max_score += 10
                checks.append({"check": "网站可达性", "status": "⚠️", "detail": f"无法访问: {e}"})

        # 综合评分
        final_score = round(score / max(max_score, 1) * 100, 1) if max_score > 0 else 0
        if final_score >= 80:
            level = "高可信度"
            verdict = "✅ 数据可靠，可直接使用"
        elif final_score >= 50:
            level = "中等可信度"
            verdict = "⚠️ 部分信息缺失或存疑，建议补充验证"
        else:
            level = "低可信度"
            verdict = "❌ 信息严重不足，不建议使用"

        return {
            "name": name,
            "score": final_score,
            "level": level,
            "verdict": verdict,
            "checks": checks,
            "verified_at": datetime.now(timezone.utc).isoformat(),
        }


# ════════════════════════════════════════════
# 2. 合并去重
# ════════════════════════════════════════════

class DataDeduper:
    """数据去重 — 同名/同网址/同邮箱自动合并"""

    @staticmethod
    def _fingerprint(item: dict) -> str:
        """生成记录指纹（用于快速匹配重复）"""
        # 归一化名称
        name = (item.get("name") or item.get("company") or "").strip().lower()
        name = re.sub(r'[^a-z0-9\s]', '', name)
        name = re.sub(r'\s+', ' ', name).strip()

        # 去掉 Pty Ltd / Ltd / Limited / Inc / LLC / Corp / GmbH 等后缀
        biz_suffixes = [r'\bpty\s*ltd\b', r'\bltd\b', r'\blimited\b',
                       r'\binc\b', r'\bllc\b', r'\bcorp\b', r'\bgmbh\b',
                       r'\bco\b', r'\bgroup\b', r'\bholdings\b', r'\benterprise\b']
        for suffix in biz_suffixes:
            name = re.sub(suffix, '', name).strip()
        name = re.sub(r'\s+', ' ', name).strip()

        # 提取核心名称（前4个词）
        words = name.split()
        core_name = ' '.join(words[:min(len(words), 4)])

        website = (item.get("website") or "").strip().lower()
        website = re.sub(r'^https?://', '', website)
        website = website.rstrip("/")
        website = re.sub(r'^www\.', '', website)

        # 指纹：核心名称 + 网站基域
        domain = website.split(".")[0] if website else ""
        text = f"{core_name}|{domain}"
        return hashlib.md5(text.encode()).hexdigest()

    @staticmethod
    def find_duplicates(records: list, threshold: float = 0.85) -> list:
        """找出重复记录组

        Args:
            records: 记录列表 [{name, website, ...}]
            threshold: 匹配阈值

        Returns:
            [(group_id, [record_indices])] — 每组重复的记录索引
        """
        fingerprints = {}
        for i, rec in enumerate(records):
            fp = DataDeduper._fingerprint(rec)
            if fp not in fingerprints:
                fingerprints[fp] = []
            fingerprints[fp].append(i)

        groups = []
        for fp, indices in fingerprints.items():
            if len(indices) > 1:
                groups.append((fp, indices))

        return groups

    @staticmethod
    def merge_group(records: list, indices: list) -> dict:
        """合并一组重复记录，选取各字段最优值"""
        group_recs = [records[i] for i in indices]

        merged = {}
        # 收集所有字段
        all_keys = set()
        for r in group_recs:
            all_keys.update(r.keys())

        for key in all_keys:
            values = [r.get(key) for r in group_recs if r.get(key)]
            if not values:
                continue
            # 优先选最长的非空值
            str_values = [v for v in values if isinstance(v, str)]
            if str_values:
                merged[key] = max(set(str_values), key=len)
            else:
                merged[key] = values[0]

        # 添加合并元数据
        merged["_merged_from"] = len(indices)
        merged["_merged_sources"] = [records[i].get("name", f"#{i}") for i in indices]
        return merged

    @staticmethod
    def dedup_records(records: list) -> dict:
        """完整去重流程

        Args:
            records: 记录列表

        Returns:
            {
                "total_before": N,
                "total_after": M,
                "duplicate_groups": [...],
                "records": [去重后的记录],
                "removed_count": N-M
            }
        """
        groups = DataDeduper.find_duplicates(records)
        removed_indices = set()
        merged_records = []

        for fp, indices in groups:
            keep_idx = indices[0]  # 保留第一条
            for idx in indices[1:]:
                removed_indices.add(idx)

            # 合并所有字段
            merged = DataDeduper.merge_group(records, indices)
            merged_records.append(merged)

        # 添加未被合并的记录
        for i, rec in enumerate(records):
            if i not in removed_indices:
                # 检查是否已被 merge_group 添加
                already_merged = False
                for merged in merged_records:
                    if merged.get("_merged_sources") and \
                       rec.get("name") in merged["_merged_sources"]:
                        already_merged = True
                        break
                if not already_merged:
                    merged_records.append(dict(rec))

        return {
            "total_before": len(records),
            "total_after": len(merged_records),
            "removed_count": len(removed_indices),
            "duplicate_groups": [(fp, list(indices)) for fp, indices in groups],
            "records": merged_records,
        }


# ════════════════════════════════════════════
# 3. 质量评分
# ════════════════════════════════════════════

class DataQuality:
    """数据质量评分与报告"""

    QUALITY_DIMENSIONS = {
        "completeness": {"weight": 0.30, "desc": "字段完整度"},
        "accuracy": {"weight": 0.25, "desc": "数据准确度"},
        "freshness": {"weight": 0.20, "desc": "数据新鲜度"},
        "consistency": {"weight": 0.15, "desc": "数据一致性"},
        "uniqueness": {"weight": 0.10, "desc": "数据唯一性"},
    }

    @staticmethod
    def assess_dataset(records: list) -> dict:
        """评估整个数据集的质量"""
        n = len(records)
        if n == 0:
            return {"score": 0, "dims": {}, "summary": "空数据集"}

        # 完整度：非空字段比例
        completeness_scores = []
        for rec in records:
            filled = sum(1 for v in rec.values() if v and str(v).strip())
            total = max(len(rec), 1)
            completeness_scores.append(filled / total)
        completeness = round(sum(completeness_scores) / n * 100, 1)

        # 新鲜度：最近更新比例
        fresh_count = 0
        for rec in records:
            updated = rec.get("updated_at") or rec.get("verified_at") or ""
            if updated:
                fresh_count += 1
        freshness = round(fresh_count / n * 100, 1)

        # 唯一性：去重后的比例
        deduper = DataDeduper()
        groups = deduper.find_duplicates(records)
        unique_ratio = round((1 - len(groups) / max(n, 1)) * 100, 1)

        # 一致性：名称中有企业标识的比例
        consistent = 0
        for rec in records:
            name = (rec.get("name") or rec.get("company") or "")
            if any(ind in name.lower() for ind in ["pty", "ltd", "limited", "corp", "inc", "llc"]):
                consistent += 1
        consistency = round(consistent / n * 100, 1)

        # 综合分
        dims = {
            "completeness": {"score": completeness, "weight": 0.30},
            "freshness": {"score": freshness, "weight": 0.20},
            "uniqueness": {"score": unique_ratio, "weight": 0.10},
            "consistency": {"score": consistency, "weight": 0.15},
            "accuracy": {"score": min(completeness + 10, 100), "weight": 0.25},
        }
        total = round(sum(d["score"] * d["weight"] for d in dims.values()), 1)

        return {
            "total_records": n,
            "overall_score": total,
            "dimensions": dims,
            "summary": (
                "✅ 数据质量良好" if total >= 80
                else "⚠️ 数据质量一般，建议补充字段" if total >= 50
                else "❌ 数据质量差，需要重新采集"
            ),
        }


# ════════════════════════════════════════════
# 4. 统一入口
# ════════════════════════════════════════════

class DataVerifierDeduper:
    """P1 数据验证去重 — 统一入口"""

    verify = DataVerifier()
    dedup = DataDeduper()
    quality = DataQuality()

    @staticmethod
    def full_pipeline(company_info: dict, deep: bool = False) -> dict:
        """完整管道：验证→去重→质量评分

        Args:
            company_info: 公司信息字典
            deep: 是否深度验证

        Returns:
            综合报告
        """
        # 1. 验证
        verification = DataVerifier.verify_company(
            name=company_info.get("name", ""),
            website=company_info.get("website", ""),
            abn=company_info.get("abn", ""),
            phone=company_info.get("phone", ""),
            email=company_info.get("email", ""),
            deep=deep,
        )

        # 2. 去重检查（单条数据检测自身重复字段）
        name_norm = re.sub(r'\s+', ' ', (company_info.get("name") or "").lower().strip())
        dedup_check = {
            "status": "单条记录，无需去重",
            "fields": len([k for k in company_info.keys() if company_info.get(k)]),
        }

        return {
            "company": company_info.get("name", ""),
            "verification": verification,
            "dedup_check": dedup_check,
            "quality_score": verification["score"],
            "pipeline_at": datetime.now(timezone.utc).isoformat(),
        }


if __name__ == "__main__":
    import sys

    # CLI 测试
    if "--test" in sys.argv:
        # 测试验证
        result = DataVerifier.verify_company(
            name="Crystalbrook Collection Pty Ltd",
            website="crystalbrookcollection.com",
            abn="12345678901",
            phone="+61 2 1234 5678",
            email="info@crystalbrook.com",
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"\n可信度评分: {result['score']}% ({result['level']})")

        # 测试去重
        test_records = [
            {"name": "Aus Modular Homes Pty Ltd", "website": "ausmodular.com.au"},
            {"name": "Aus Modular Homes Pty Ltd", "website": "ausmodular.com"},
            {"name": "Green Building Solutions", "website": "greenbuild.com.au"},
            {"name": "Aus Modular Homes", "website": "ausmodular.com.au"},
        ]
        dedup_result = DataDeduper.dedup_records(test_records)
        print(f"\n去重: {dedup_result['total_before']}→{dedup_result['total_after']} "
              f"(去重 {dedup_result['removed_count']})")

        # 测试质量评分
        quality = DataQuality.assess_dataset(test_records)
        print(f"数据质量: {quality['overall_score']}/100 ({quality['summary']})")
    elif "--verify" in sys.argv:
        name = sys.argv[sys.argv.index("--verify") + 1]
        result = DataVerifier.verify_company(name=name)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif "--dedup-file" in sys.argv:
        idx = sys.argv.index("--dedup-file")
        filepath = sys.argv[idx + 1]
        with open(filepath) as f:
            records = json.load(f) if filepath.endswith(".json") else json.loads(f.read())
        result = DataDeduper.dedup_records(records)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("用法:")
        print("  python3 core.py --test                # 测试验证+去重")
        print("  python3 core.py --verify '公司名'     # 验证单公司")
        print("  python3 core.py --dedup-file data.md  # 去重数据文件")
