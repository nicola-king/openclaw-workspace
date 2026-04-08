#!/usr/bin/env python3
"""
知几-E 连败计数器重置脚本
用途：手动重置连败保护，恢复交易

使用方法:
    python3 reset-zhiji-loss-counter.py
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime

# 配置
DB_PATH = Path("/home/nicola/.openclaw/workspace/data/zhiji-paper-trading.db")
STATE_FILE = Path("/home/nicola/.openclaw/workspace/logs/paper-trading-state.json")

def reset_loss_counter():
    """重置连败计数器"""
    print("🔄 开始重置知几-E 连败计数器...")
    
    # 方法 1: 重置状态文件
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
        
        old_count = state.get('consecutive_losses', 0)
        state['consecutive_losses'] = 0
        state['last_loss_reset'] = datetime.now().isoformat()
        state['reset_reason'] = '手动重置 (新一天开始)'
        
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 状态文件已重置：连败 {old_count} → 0")
    else:
        # 创建新状态
        state = {
            'consecutive_losses': 0,
            'last_loss_reset': datetime.now().isoformat(),
            'reset_reason': '手动重置 (新一天开始)',
            'total_trades': 400,
            'balance': 105871350.66
        }
        STATE_FILE.parent.mkdir(exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        print(f"✅ 状态文件已创建")
    
    # 方法 2: 重置数据库 (如果存在)
    if DB_PATH.exists():
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # 查找并更新配置表
            cursor.execute("""
                UPDATE config 
                SET value = '0' 
                WHERE key = 'consecutive_losses'
            """)
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ 数据库已重置：{cursor.rowcount} 行更新")
            else:
                print("ℹ️  数据库中无连败计数配置")
            
            conn.close()
        except Exception as e:
            print(f"⚠️  数据库重置失败：{e}")
    else:
        print("ℹ️  数据库不存在，跳过")
    
    print("\n🎉 重置完成！知几-E 已恢复交易能力")
    print(f"⏰ 重置时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n下一步:")
    print("1. 运行模拟盘验证：python3 scripts/zhiji-e-paper-trading-offline.py")
    print("2. 检查是否还有'连败保护'提示")

if __name__ == '__main__':
    reset_loss_counter()
