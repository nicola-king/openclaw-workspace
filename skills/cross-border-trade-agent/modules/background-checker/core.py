#!/usr/bin/env python3
"""
外贸背调 (Background Checker) v1.0.0
基于"不背调就不要做外贸"五步法：
1. Whois域名查询 — 查域名注册时间、国家、邮箱
2. 官网+地图验证 — Google Maps实景、LinkedIn资料
3. Panjiva — 专业海关数据（需 API Key，当前占位）
4. ImportYeti — 免费海关数据
5. ZoomInfo — 邮箱/公司验证（需 API Key，当前占位）

集成到公司富化 pipeline，输出可信度评分 A/B/C/D
"""

import json
import logging
import socket
import re
import sqlite3
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from urllib.parse import urlparse, quote

# optional whois
try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("background-checker")


class BackgroundChecker:
    """外贸背调五步法"""

    # 可信度评分标准
    RISK_LABELS = {
        'A': '✅ 高度可信 — 信息完整匹配，无风险信号',
        'B': '⚠️ 基本可信 — 信息基本完整，需人工核实',
        'C': '⚠️ 需关注 — 信息缺失或有疑点，建议谨慎',
        'D': '🚨 高风险 — 存在明显风险信号，不建议合作',
    }

    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(
            Path.home() / '.openclaw' / 'workspace' / 'data' / 'cross-border-trade-agent' / 'company-enricher' / 'companies.db'
        )

    def verify_domain(self, domain: str) -> Dict[str, Any]:
        """
        第一步：Whois 域名查询
        查注册时间、所属国家、注册邮箱，辨别网站真伪
        """
        result = {
            'domain': domain,
            'registered': None,
            'registrar': None,
            'country': None,
            'registrant_email': None,
            'creation_date': None,
            'expiration_date': None,
            'days_since_creation': None,
            'risk_flags': [],
            'risk_score': 0,
            'source': 'whois',
        }

        if not WHOIS_AVAILABLE:
            result['error'] = 'python-whois 未安装'
            return result

        try:
            import socket
            socket.setdefaulttimeout(8)  # Whois 超时保护
            w = whois.whois(domain)
            socket.setdefaulttimeout(None)
            creation = w.creation_date
            if isinstance(creation, list):
                creation = creation[0]
            if isinstance(creation, datetime):
                result['creation_date'] = creation.isoformat()
                days = (datetime.now(timezone.utc) - creation).days
                result['days_since_creation'] = days
                if days < 180:
                    result['risk_flags'].append(f'域名注册不足6个月（{days}天）')
                    result['risk_score'] += 30
                elif days < 365:
                    result['risk_flags'].append(f'域名注册不足1年（{days}天）')
                    result['risk_score'] += 10
                else:
                    result['registered'] = f'✅ {days}天前注册'
            else:
                result['registered'] = f'注册时间: {creation}'

            # 国家
            country = w.get('country')
            if country:
                result['country'] = country if isinstance(country, str) else str(country)
            else:
                result['risk_flags'].append('域名所属国家不可查')
                result['risk_score'] += 5

            # 注册邮箱
            email = w.get('emails')
            if email:
                if isinstance(email, list):
                    email = email[0]
                result['registrant_email'] = email
                # 检测临时邮箱
                if email and re.search(r'(mailinator|guerrillamail|tempmail|10minutemail)', str(email), re.I):
                    result['risk_flags'].append('使用临时邮箱注册域名')
                    result['risk_score'] += 40

            # 注册商
            registrar = w.get('registrar')
            if registrar:
                result['registrar'] = registrar if isinstance(registrar, str) else str(registrar)

        except Exception as e:
            result['error'] = f'Whois 查询失败: {str(e)[:100]}'
            result['risk_flags'].append('域名信息无法查询')
            result['risk_score'] += 25

        return result

    def verify_website(self, company_name: str, website: str) -> Dict[str, Any]:
        """
        第二步：官网验证
        核实官网真实性、SSL、基本信息匹配
        """
        result = {
            'company_name': company_name,
            'website': website,
            'www_resolves': False,
            'has_ssl': False,
            'page_contains_company': False,
            'risk_flags': [],
            'risk_score': 0,
        }

        if not website:
            result['risk_flags'].append('无官网')
            result['risk_score'] += 30
            return result

        # 标准化域名
        domain = website.strip()
        if not domain.startswith('http'):
            domain = 'https://' + domain
        parsed = urlparse(domain)
        hostname = parsed.hostname or domain

        # DNS 解析检查
        try:
            socket.getaddrinfo(hostname, 80)
            result['www_resolves'] = True
        except Exception:
            result['risk_flags'].append('域名无法解析')
            result['risk_score'] += 20

        # SSL 检查（简单通过 https 判断）
        if parsed.scheme == 'https' or website.startswith('https'):
            result['has_ssl'] = True

        # 网站是否包含公司名（简单检查）
        try:
            import urllib.request
            req = urllib.request.Request(f'https://{hostname}', headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
            }, method='GET')
            with urllib.request.urlopen(req, timeout=5) as resp:
                html = resp.read().decode('utf-8', errors='replace')[:10000]
                # 检查公司名是否出现在页面中
                name_parts = [p for p in re.split(r'[（( ,]', company_name) if len(p) > 2]
                if name_parts:
                    match_count = sum(1 for p in name_parts if p.lower() in html.lower())
                    if match_count >= 1:
                        result['page_contains_company'] = True
        except Exception:
            pass

        return result

    def verify_customs(self, company_name: str, country: str = None) -> Dict[str, Any]:
        """
        第三步：海关贸易数据查询
        免费开源替代方案：
        - US Census Bureau International Trade API（免费，无需Key）
        - Trade.gov API（免费，需注册获取免费Key）
        - 原 Panjiva/ImportYeti 保留占位
        """
        result = {
            'company_name': company_name,
            'country': country,
            'panjiva': {'available': False, 'note': '🔓 开源替代: US Census Trade API（免费，无需API Key）'},
            'trade_census': {'available': False, 'data': None, 'note': ''},
            'risk_flags': [],
            'risk_score': 0,
        }

        # 免费方案①：US Census Bureau API（免费开放数据）
        try:
            import urllib.request
            import json as json_module
            # US Census International Trade Data API
            # https://api.census.gov/data/timeseries/intltrade/imports/exports
            census_url = ('https://api.census.gov/data/timeseries/intltrade/exports/enduse?'
                          f'get=CTY_NAME,ALL_VAL_MO&CTY_NAME={quote(company_name[:20])}'
                          '&time=2025&key=')
            req = urllib.request.Request(census_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                census_data = json_module.loads(resp.read())
                if len(census_data) > 1:
                    rows = census_data[1:]  # 第一行是header
                    result['trade_census']['available'] = True
                    result['trade_census']['data'] = rows[:5]
                    result['trade_census']['note'] = f'US Census 查到 {len(rows)} 条贸易记录'
                    result['risk_score'] -= 10  # 有贸易记录，降低风险
                else:
                    result['trade_census']['note'] = 'US Census 未找到该公司的贸易记录'
        except Exception as e:
            result['trade_census']['note'] = f'US Census 查询: {str(e)[:50]}'

        # 免费方案②：通过 Trade.gov API 查询市场情报
        try:
            # Trade.gov Market Intelligence API（免费注册获取Key）
            # 这里用公开可访问的 endpoints
            trade_url = f'https://api.trade.gov/v1/trade_events/search?q={quote(company_name[:20])}'
            req = urllib.request.Request(trade_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                trade_data = json_module.loads(resp.read())
                if trade_data.get('count', 0) > 0:
                    result['trade_census']['note'] += f' | Trade.gov {trade_data["count"]} 条'
        except Exception:
            pass

        # 保留原 ImportYeti 查询
        try:
            importyeti_url = f'https://www.importyeti.com/search?q={quote(company_name[:30])}'
            req = urllib.request.Request(importyeti_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                html = resp.read().decode('utf-8', errors='replace')
                if 'results' in html.lower() or company_name[:10].lower() in html.lower():
                    result['panjiva']['available'] = True
                    result['panjiva']['note'] = 'ImportYeti 有搜索结果，建议浏览器打开查看: https://www.importyeti.com'
        except Exception:
            pass

        return result

    def verify_email(self, email: str) -> Dict[str, Any]:
        """
        第五步：邮箱验证
        免费开源方案：
        - Trumail（1050⭐，Go编写，免费自托管）
        - KnowEmail（Python，批量验证）
        - Python smtplib + DNS 基础验证
        """
        result = {
            'email': email,
            'format_valid': False,
            'has_mx': False,
            'disposable': False,
            'smtp_check': False,
            'risk_flags': [],
            'risk_score': 0,
        }

        if not email:
            result['risk_flags'].append('无邮箱')
            result['risk_score'] += 20
            return result

        # 格式验证
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            result['format_valid'] = True
        else:
            result['risk_flags'].append(f'邮箱格式异常: {email}')
            result['risk_score'] += 15
            return result

        # 一次性邮箱检测
        disposable_domains = [
            'mailinator.com', 'guerrillamail.com', 'tempmail.com', '10minutemail.com',
            'yopmail.com', 'throwaway.com', 'sharklasers.com', 'trashmail.com',
            'mailnator.com', 'getairmail.com', 'temp-mail.org'
        ]
        domain = email.split('@')[1].lower()
        if domain in disposable_domains or any(d in domain for d in ['temp', 'throw', 'trash', 'fake']):
            result['disposable'] = True
            result['risk_flags'].append('检测到临时/一次性邮箱')
            result['risk_score'] += 40

        # MX 记录检测
        try:
            import dns.resolver
            mx_records = dns.resolver.resolve(domain, 'MX')
            if mx_records:
                result['has_mx'] = True
                result['mx_servers'] = [str(r.exchange) for r in mx_records[:3]]
        except ImportError:
            # 没有 dnspython，用 socket 简单检查
            try:
                import socket
                socket.getaddrinfo(domain, 25)
                result['has_mx'] = True
            except Exception:
                result['risk_flags'].append('无法解析邮箱域名MX记录')
                result['risk_score'] += 10
        except Exception:
            result['risk_flags'].append('邮箱域名似乎无效（无MX记录）')
            result['risk_score'] += 10

        # 建议（占位 - Trumail/KnowEmail 可自托管实现 SMTP 验证）
        result['smtp_note'] = (
            '如需更精准的 SMTP 验证，可自托管以下开源项目:\n'
            '  - Trumail (1050⭐): https://github.com/trumail/trumail (Go)\n'
            '  - KnowEmail (Python): https://github.com/OpenInitia/KnowEmail'
        )

        return result

    def generate_risk_score(self, whois_result: Dict, website_result: Dict,
                             customs_result: Dict,
                             email_result: Dict = None) -> Tuple[str, int, List[str]]:
        """
        综合评分：A/B/C/D
        整合五步法结果
        """
        total = 0
        flags = []

        total += whois_result.get('risk_score', 0)
        total += website_result.get('risk_score', 0)
        total += customs_result.get('risk_score', 0)

        if email_result:
            total += email_result.get('risk_score', 0)

        flags.extend(whois_result.get('risk_flags', []))
        flags.extend(website_result.get('risk_flags', []))
        flags.extend(customs_result.get('risk_flags', []))

        if email_result:
            flags.extend(email_result.get('risk_flags', []))

        # 加分项（降低风险）
        bonus = 0
        if whois_result.get('days_since_creation') and whois_result['days_since_creation'] > 365:
            bonus -= 15  # 域名超过1年，可信
        if website_result.get('www_resolves'):
            bonus -= 10
        if website_result.get('page_contains_company'):
            bonus -= 15
        if website_result.get('has_ssl'):
            bonus -= 5

        total = max(0, total + bonus)

        # 评级
        if total <= 15:
            grade = 'A'
        elif total <= 35:
            grade = 'B'
        elif total <= 55:
            grade = 'C'
        else:
            grade = 'D'

        return grade, total, flags

    def check_company(self, company_name: str, website: str = None, email: str = None) -> Dict[str, Any]:
        """
        完整五步背调一个公司
        """
        logger.info(f"🔍 背调公司: {company_name}")

        result = {
            'company_name': company_name,
            'check_time': datetime.now().isoformat(),
            'website': website,
            'email': email,
            'steps': {},
            'grade': 'N/A',
            'grade_label': '数据不足',
            'total_risk_score': 0,
            'risk_flags': [],
            'recommendation': '',
        }

        # Step 1: Whois 域名查询
        if website:
            domain = urlparse('https://' + website if not website.startswith('http') else website).hostname or website
            whois_result = self.verify_domain(domain)
            result['steps']['whois'] = whois_result

        # Step 2: 官网+基础验证
        website_result = self.verify_website(company_name, website or '')
        result['steps']['website'] = website_result

        # Step 3+4: 海关贸易数据查询（免费开源替代）
        customs_result = self.verify_customs(company_name)
        result['steps']['customs'] = customs_result

        # Step 5: 邮箱验证（免费开源替代）
        email_result = self.verify_email(email or '')
        result['steps']['email'] = email_result

        # 综合评分
        grade, score, flags = self.generate_risk_score(
            whois_result if website else {},
            website_result,
            customs_result,
            email_result
        )
        result['grade'] = grade
        result['grade_label'] = self.RISK_LABELS.get(grade, '未知')
        result['total_risk_score'] = score
        result['risk_flags'] = flags

        # 建议
        if grade == 'A':
            result['recommendation'] = '✅ 可直接合作，信息完整可信'
        elif grade == 'B':
            result['recommendation'] = '⚠️ 可初步接触，建议电话/视频核实后再深入'
        elif grade == 'C':
            result['recommendation'] = '⚠️ 建议先小额试单，或要求对方提供更多资质证明'
        else:
            result['recommendation'] = '🚨 强烈不建议合作。如需推进，必须实地考察+第三方担保'

        return result

    def batch_check(self, companies: List[Dict]) -> List[Dict]:
        """批量背调"""
        results = []
        for c in companies:
            r = self.check_company(
                c.get('name', c.get('company_name', '')),
                c.get('website', '')
            )
            results.append(r)
        return results


def main():
    """命令行入口"""
    import argparse
    parser = argparse.ArgumentParser(description='外贸背调五步法')
    parser.add_argument('--company', '-c', help='公司名称')
    parser.add_argument('--website', '-w', help='公司网站')
    parser.add_argument('--email', '-e', help='联系邮箱')
    parser.add_argument('--batch', '-b', help='批量查询 JSON 文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径',
                        default='exports/background-check-result.json')

    args = parser.parse_args()

    checker = BackgroundChecker()

    if args.batch:
        with open(args.batch, 'r', encoding='utf-8') as f:
            companies = json.load(f)
        results = checker.batch_check(companies)
    elif args.company:
        result = checker.check_company(args.company, args.website, args.email)
        results = [result]
    else:
        # 演示：查一个示例公司
        result = checker.check_company("Example Trading Corp", "example.com", "contact@example.com")
        results = [result]

    output = json.dumps(results, ensure_ascii=False, indent=2, default=str)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"✅ 结果已保存: {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
