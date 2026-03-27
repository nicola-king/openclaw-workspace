#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Steward (管家) - 用户管理 Bot
职责：付费用户管理 + 订阅跟踪 + 交付自动化
"""

import os
import sys
import sqlite3
import logging
from datetime import datetime, timedelta
from flask import Flask, request, jsonify

# 配置
BOT_TOKEN = "8744404079:AAHcT_zYabl5Yud3aDAGd7yY1qrjXxCEaYI"
DATABASE_PATH = '/home/nicola/.openclaw/workspace/data/steward_users.db'
VIP_GROUP_ID = '@taiyi_vip'
RENEWAL_REMINDER_DAYS = 7

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/home/nicola/.openclaw/workspace/logs/steward.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('Steward')

# Flask Webhook
app = Flask(__name__)

class StewardBot:
    """管家 Bot - 用户管理专家"""
    
    def __init__(self):
        self.init_database()
        
    def init_database(self):
        """初始化用户数据库"""
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id TEXT UNIQUE,
                email TEXT UNIQUE,
                name TEXT,
                product TEXT,
                status TEXT DEFAULT 'active',
                start_date TEXT,
                end_date TEXT,
                auto_renew BOOLEAN DEFAULT True,
                gumroad_purchase_id TEXT,
                joined_vip_group BOOLEAN DEFAULT False,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                type TEXT,  -- purchase/renewal/cancellation
                amount REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized")
    
    def create_user(self, data):
        """创建新用户"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (telegram_id, email, name, product, status, 
                                   start_date, end_date, gumroad_purchase_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('telegram_id'),
                data.get('email'),
                data.get('name'),
                data.get('product', 'Hunter Pro'),
                'active',
                datetime.now().strftime('%Y-%m-%d'),
                (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                data.get('purchase_id')
            ))
            
            conn.commit()
            user_id = cursor.lastrowid
            logger.info(f"User created: {data.get('email')}")
            
            return {'id': user_id, 'email': data.get('email')}
            
        except sqlite3.IntegrityError:
            logger.warning(f"User already exists: {data.get('email')}")
            return None
        finally:
            conn.close()
    
    def update_subscription(self, data):
        """更新订阅"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET status = 'active',
                end_date = ?,
                auto_renew = True,
                updated_at = CURRENT_TIMESTAMP
            WHERE email = ?
        ''', (
            (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
            data.get('email')
        ))
        
        conn.commit()
        conn.close()
        logger.info(f"Subscription updated: {data.get('email')}")
    
    def cancel_subscription(self, data):
        """取消订阅"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET status = 'cancelled',
                auto_renew = False,
                updated_at = CURRENT_TIMESTAMP
            WHERE email = ?
        ''', (data.get('email'),))
        
        conn.commit()
        conn.close()
        logger.info(f"Subscription cancelled: {data.get('email')}")
    
    def check_expiring_subscriptions(self):
        """检查到期订阅 (每日执行)"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        expiry_date = (datetime.now() + timedelta(days=RENEWAL_REMINDER_DAYS)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT * FROM users 
            WHERE end_date = ? AND status = 'active'
        ''', (expiry_date,))
        
        expiring_users = cursor.fetchall()
        conn.close()
        
        for user in expiring_users:
            logger.info(f"Sending renewal reminder to: {user[2]}")
            # TODO: 发送续费提醒消息
        
        return expiring_users
    
    def check_expired_subscriptions(self):
        """检查过期订阅 (每日执行)"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT * FROM users 
            WHERE end_date < ? AND status = 'active'
        ''', (today,))
        
        expired_users = cursor.fetchall()
        conn.close()
        
        for user in expired_users:
            logger.info(f"Subscription expired: {user[2]}")
            # TODO: 降级到免费 + 移除 VIP 群
        
        return expired_users
    
    def generate_daily_report(self):
        """生成日报表"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        today = datetime.now().date()
        
        # 统计
        cursor.execute('SELECT COUNT(*) FROM users WHERE DATE(created_at) = ?', (today,))
        new_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'active'")
        active_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM transactions WHERE DATE(timestamp) = ?', (today,))
        today_transactions = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(amount) FROM transactions WHERE DATE(timestamp) = ?', (today,))
        today_revenue = cursor.fetchone()[0] or 0
        
        conn.close()
        
        report = f"""
【管家日报 · {today}】

新增用户：{new_users}
活跃用户：{active_users}
今日交易：{today_transactions}
今日收入：${today_revenue:.2f}

━━━━━━━━━━━━━━━━━━━━━

【产品分布】
Hunter Pro: 待统计
PolyAlert Pro: 待统计

━━━━━━━━━━━━━━━━━━━━━

*数据截止：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        logger.info(f"Daily report generated: {report}")
        return report


# Gumroad Webhook
@app.route('/webhook/gumroad', methods=['POST'])
def gumroad_webhook():
    """处理 Gumroad Webhook"""
    data = request.json
    logger.info(f"Gumroad webhook received: {data}")
    
    steward = StewardBot()
    
    if data.get('event') == 'purchase':
        # 新用户购买
        user_data = {
            'telegram_id': data.get('custom_fields', {}).get('telegram_id'),
            'email': data.get('email'),
            'name': data.get('full_name'),
            'product': data.get('product_name'),
            'purchase_id': data.get('id')
        }
        user = steward.create_user(user_data)
        
        if user:
            logger.info(f"New purchase: {user['email']}")
            # TODO: 发送欢迎消息 + 邀请 VIP 群
        
    elif data.get('event') == 'subscription_renewal':
        # 续费成功
        steward.update_subscription(data)
        logger.info(f"Subscription renewed: {data.get('email')}")
        
    elif data.get('event') == 'subscription_cancelled':
        # 订阅取消
        steward.cancel_subscription(data)
        logger.info(f"Subscription cancelled: {data.get('email')}")
    
    return jsonify({'status': 'success'}), 200


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({'status': 'healthy', 'service': 'steward'}), 200


if __name__ == '__main__':
    logger.info("Steward Bot starting...")
    
    # 初始化数据库
    steward = StewardBot()
    
    # 启动 Webhook 服务器
    logger.info("Starting Gumroad webhook server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)
