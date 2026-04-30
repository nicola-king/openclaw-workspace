#!/usr/bin/env python3
"""
🔧 修复微信投递队列

功能:
- 检查失败的投递
- 添加正确的 accountId
- 移动到待投递队列
- 激活微信会话

作者：太一 AGI
创建：2026-04-11
"""

import json
import shutil
from pathlib import Path
from datetime import datetime


class WechatDeliveryFixer:
    """微信投递修复器"""
    
    def __init__(self):
        """初始化修复器"""
        self.failed_dir = Path("/home/nicola/.openclaw/delivery-queue/failed")
        self.pending_dir = Path("/home/nicola/.openclaw/delivery-queue/pending")
        self.weixin_accounts_dir = Path("/home/nicola/.openclaw/openclaw-weixin/accounts")
        
        self.pending_dir.mkdir(parents=True, exist_ok=True)
        
        print("🔧 微信投递修复器已初始化")
        print()
    
    def load_accounts(self) -> dict:
        """加载微信账户"""
        accounts = {}
        
        for account_file in self.weixin_accounts_dir.glob("*-im-bot.json"):
            if "context-tokens" not in account_file.name and "sync" not in account_file.name:
                account_id = account_file.stem.replace("-im-bot", "")
                
                with open(account_file, 'r', encoding='utf-8') as f:
                    account_data = json.load(f)
                
                accounts[account_id] = {
                    "token": account_data.get('token', ''),
                    "userId": account_data.get('userId', ''),
                    "baseUrl": account_data.get('baseUrl', ''),
                    "savedAt": account_data.get('savedAt', '')
                }
        
        print(f"✅ 加载到 {len(accounts)} 个微信账户")
        for acc_id, acc_data in accounts.items():
            print(f"   - {acc_id}: {acc_data['userId'][:20]}...")
        
        return accounts
    
    def fix_delivery(self, delivery_file: Path, accounts: dict) -> bool:
        """修复单个投递"""
        with open(delivery_file, 'r', encoding='utf-8') as f:
            delivery = json.load(f)
        
        # 检查是否已有 accountId
        if not delivery.get('accountId'):
            # 选择第一个账户
            if accounts:
                account_id = list(accounts.keys())[0]
                delivery['accountId'] = account_id
                print(f"   ✅ 添加 accountId: {account_id}")
            else:
                print(f"   ❌ 无可用账户")
                return False
        
        # 重置重试计数
        delivery['retryCount'] = 0
        delivery['lastAttemptAt'] = None
        delivery['lastError'] = None
        delivery['status'] = 'pending_retry'
        delivery['fixedAt'] = datetime.now().isoformat()
        
        # 移动到待投递队列
        pending_file = self.pending_dir / delivery_file.name
        with open(pending_file, 'w', encoding='utf-8') as f:
            json.dump(delivery, f, ensure_ascii=False, indent=2)
        
        # 删除原文件
        delivery_file.unlink()
        
        print(f"   ✅ 已移动到待投递队列：{pending_file.name}")
        return True
    
    def fix_all(self) -> dict:
        """修复所有失败投递"""
        accounts = self.load_accounts()
        
        failed_files = list(self.failed_dir.glob("*.json"))
        
        print(f"\n📊 发现 {len(failed_files)} 个失败投递")
        print()
        
        results = {
            "total": len(failed_files),
            "fixed": 0,
            "failed": 0,
            "details": []
        }
        
        for delivery_file in failed_files:
            print(f"修复：{delivery_file.name}")
            
            if self.fix_delivery(delivery_file, accounts):
                results["fixed"] += 1
                results["details"].append({
                    "file": delivery_file.name,
                    "status": "fixed"
                })
            else:
                results["failed"] += 1
                results["details"].append({
                    "file": delivery_file.name,
                    "status": "failed"
                })
        
        return results
    
    def generate_report(self, results: dict) -> str:
        """生成修复报告"""
        report = []
        report.append("# 🔧 微信投递修复报告")
        report.append("")
        report.append(f"**修复时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        report.append("## 修复结果")
        report.append("")
        report.append(f"- 总计：{results['total']} 个")
        report.append(f"- 成功：{results['fixed']} 个")
        report.append(f"- 失败：{results['failed']} 个")
        report.append("")
        report.append("## 详细信息")
        report.append("")
        report.append("| 文件 | 状态 |")
        report.append("|------|------|")
        
        for detail in results["details"]:
            status_emoji = "✅" if detail["status"] == "fixed" else "❌"
            report.append(f"| {detail['file']} | {status_emoji} {detail['status']} |")
        
        report.append("")
        report.append("## 下一步")
        report.append("")
        report.append("1. 检查待投递队列：`ls /home/nicola/.openclaw/delivery-queue/pending/`")
        report.append("2. 激活微信会话：`openclaw channels login`")
        report.append("3. 等待 Gateway 自动投递")
        report.append("")
        
        return "\n".join(report)


def main():
    """主函数"""
    print("="*60)
    print("🔧 微信投递修复器")
    print("="*60)
    
    fixer = WechatDeliveryFixer()
    
    # 修复所有
    print("\n1. 修复所有失败投递...")
    results = fixer.fix_all()
    
    # 生成报告
    print("\n2. 生成修复报告...")
    report = fixer.generate_report(results)
    
    report_file = Path("/home/nicola/.openclaw/workspace/reports/wechat-delivery-fix-report.md")
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 报告已保存：{report_file}")
    
    print("\n" + "="*60)
    print("✅ 微信投递修复完成!")
    print("="*60)
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
