#!/usr/bin/env python3
"""
安卓 3D 高斯泼溅测试 - 执行脚本
太一 AGI · 2026-04-18

功能:
- 创建测试目录
- 生成测试清单
- 自动记录时间
- 生成测试报告
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
TEST_DIR = WORKSPACE / "3d-gaussian-splatting" / "android-test"
OUTPUT_DIR = TEST_DIR / "output"

# 确保目录存在
for dir_path in [TEST_DIR, OUTPUT_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


class AndroidTest:
    """安卓测试记录"""
    
    def __init__(self):
        self.test_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = datetime.now()
        self.report = {
            "test_id": self.test_id,
            "start_time": self.start_time.isoformat(),
            "device": {},
            "app": "",
            "object": "",
            "capture": {},
            "timing": {},
            "quality": {},
            "issues": [],
            "recommendation": "",
        }
    
    def input_device_info(self):
        """输入设备信息"""
        print("\n📱 设备信息")
        self.report["device"]["model"] = input("手机型号：")
        self.report["device"]["android_version"] = input("Android 版本：")
    
    def input_app_info(self):
        """输入 App 信息"""
        print("\n📲 使用 App")
        print("1. KIRI Engine")
        print("2. Scaniverse")
        print("3. Polycam")
        print("4. Luma AI")
        choice = input("选择 (1-4): ")
        
        apps = {
            "1": "KIRI Engine",
            "2": "Scaniverse",
            "3": "Polycam",
            "4": "Luma AI"
        }
        self.report["app"] = apps.get(choice, "Unknown")
    
    def input_object_info(self):
        """输入测试物体信息"""
        print("\n🎯 测试物体")
        print("1. 水杯/马克杯")
        print("2. 玩具/手办")
        print("3. 盆栽植物")
        print("4. 鞋子")
        print("5. 包包")
        print("6. 其他")
        choice = input("选择 (1-6): ")
        
        objects = {
            "1": "水杯",
            "2": "玩具",
            "3": "盆栽",
            "4": "鞋子",
            "5": "包包",
            "6": input("请输入：")
        }
        self.report["object"] = objects.get(choice, "Unknown")
    
    def input_capture_info(self):
        """输入拍摄信息"""
        print("\n📸 拍摄信息")
        print("1. 视频")
        print("2. 照片")
        mode = input("模式 (1-2): ")
        
        self.report["capture"]["mode"] = "视频" if mode == "1" else "照片"
        
        if mode == "1":
            self.report["capture"]["video_duration"] = int(input("视频时长 (秒): "))
        else:
            self.report["capture"]["photo_count"] = int(input("照片数量："))
    
    def record_timing(self, step_name):
        """记录时间节点"""
        now = datetime.now()
        if "steps" not in self.report["timing"]:
            self.report["timing"]["steps"] = []
        
        self.report["timing"]["steps"].append({
            "name": step_name,
            "time": now.isoformat(),
        })
    
    def input_quality(self):
        """输入质量评估"""
        print("\n📊 质量评估 (1-5 星)")
        
        self.report["quality"]["completeness"] = int(input("完整性 (1-5): "))
        self.report["quality"]["clarity"] = int(input("清晰度 (1-5): "))
        self.report["quality"]["color"] = int(input("色彩 (1-5): "))
        self.report["quality"]["detail"] = int(input("细节 (1-5): "))
        self.report["quality"]["overall"] = int(input("整体 (1-5): "))
    
    def input_issues(self):
        """输入问题记录"""
        print("\n⚠️  问题记录 (直接回车跳过)")
        
        while True:
            issue = input("问题：")
            if not issue:
                break
            self.report["issues"].append(issue)
    
    def input_recommendation(self):
        """输入推荐意见"""
        print("\n🎊 测试结论")
        print("1. 强烈推荐")
        print("2. 推荐")
        print("3. 一般")
        print("4. 不推荐")
        choice = input("选择 (1-4): ")
        
        recommendations = {
            "1": "强烈推荐",
            "2": "推荐",
            "3": "一般",
            "4": "不推荐"
        }
        self.report["recommendation"] = recommendations.get(choice, "未知")
    
    def generate_report(self):
        """生成测试报告"""
        self.report["end_time"] = datetime.now().isoformat()
        
        # 计算总耗时
        start = datetime.fromisoformat(self.report["start_time"])
        end = datetime.fromisoformat(self.report["end_time"])
        self.report["total_duration_minutes"] = round((end - start).total_seconds() / 60, 1)
        
        # 保存 JSON 报告
        json_file = OUTPUT_DIR / f"test_report_{self.test_id}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
        
        # 生成 Markdown 报告
        md_report = self._generate_md_report()
        md_file = OUTPUT_DIR / f"test_report_{self.test_id}.md"
        md_file.write_text(md_report, encoding="utf-8")
        
        print(f"\n✅ 测试报告已保存:")
        print(f"   JSON: {json_file}")
        print(f"   MD: {md_file}")
    
    def _generate_md_report(self):
        """生成 Markdown 报告"""
        r = self.report
        
        return f"""# 安卓 3D 高斯测试报告

**测试 ID**: {r['test_id']}
**测试时间**: {r['start_time']}
**总耗时**: {r.get('total_duration_minutes', 0)} 分钟

---

## 📱 设备信息

- 手机型号：{r['device'].get('model', 'N/A')}
- Android 版本：{r['device'].get('android_version', 'N/A')}
- 使用 App: {r['app']}

---

## 🎯 测试物体

物体：{r['object']}

---

## 📸 拍摄信息

模式：{r['capture'].get('mode', 'N/A')}
""" + (
            f"视频时长：{r['capture'].get('video_duration', 'N/A')}秒\n" if r['capture'].get('mode') == '视频' 
            else f"照片数量：{r['capture'].get('photo_count', 'N/A')}张\n"
        ) + f"""
---

## 📊 质量评估

| 指标 | 评分 |
|------|------|
| 完整性 | {'⭐' * r['quality'].get('completeness', 0)} |
| 清晰度 | {'⭐' * r['quality'].get('clarity', 0)} |
| 色彩 | {'⭐' * r['quality'].get('color', 0)} |
| 细节 | {'⭐' * r['quality'].get('detail', 0)} |
| 整体 | {'⭐' * r['quality'].get('overall', 0)} |

---

## ⚠️  问题记录

""" + (
            "\n".join([f"- {issue}" for issue in r['issues']]) if r['issues'] else "无\n"
        ) + f"""
---

## 🎊 测试结论

推荐度：{r['recommendation']}

---

*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""


def main():
    """主函数"""
    print("=" * 60)
    print("🤖 安卓 3D 高斯泼溅测试")
    print("=" * 60)
    
    test = AndroidTest()
    
    # 输入信息
    test.input_device_info()
    test.input_app_info()
    test.input_object_info()
    test.input_capture_info()
    
    print("\n📸 现在开始拍摄...")
    print("拍摄完成后继续")
    input("按回车继续...")
    test.record_timing("拍摄完成")
    
    print("\n⏳ 等待处理完成...")
    input("处理完成后按回车...")
    test.record_timing("处理完成")
    
    # 质量评估
    test.input_quality()
    test.input_issues()
    test.input_recommendation()
    
    # 生成报告
    test.generate_report()
    
    print("\n🎊 测试完成！")


if __name__ == "__main__":
    main()
