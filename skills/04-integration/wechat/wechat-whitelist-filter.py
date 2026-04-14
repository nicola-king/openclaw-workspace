#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信消息白名单过滤器

功能:
1. 只处理白名单内的联系人/群消息
2. 支持正则表达式匹配
3. 支持黑名单机制
4. 自动记录过滤日志

灵感：ai-wechat 项目 (白名单机制)

作者：太一 AGI
创建：2026-04-14
"""

import os
import re
import json
import logging
from typing import List, Set, Optional
from datetime import datetime
from pathlib import Path

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('WechatWhitelistFilter')


class WechatWhitelistFilter:
    """微信消息白名单过滤器"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.whitelist: Set[str] = set()  # 白名单
        self.blacklist: Set[str] = set()  # 黑名单
        self.patterns: List[re.Pattern] = []  # 正则匹配
        self.filter_log: List[dict] = []
        
        # 配置文件
        if config_file:
            self.config_file = Path(config_file)
        else:
            self.config_file = Path(__file__).parent / 'config' / 'wechat-whitelist.json'
        
        # 加载配置
        self.load_config()
    
    def load_config(self):
        """加载白名单配置"""
        if not self.config_file.exists():
            logger.warning(f"⚠️ 配置文件不存在：{self.config_file}")
            self._create_default_config()
            return
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 白名单
            self.whitelist = set(config.get('whitelist', []))
            logger.info(f"✅ 加载白名单：{len(self.whitelist)} 个")
            
            # 黑名单
            self.blacklist = set(config.get('blacklist', []))
            logger.info(f"✅ 加载黑名单：{len(self.blacklist)} 个")
            
            # 正则匹配
            patterns = config.get('patterns', [])
            self.patterns = [re.compile(p) for p in patterns]
            logger.info(f"✅ 加载正则匹配：{len(self.patterns)} 个")
            
        except Exception as e:
            logger.error(f"❌ 加载配置失败：{e}")
            self._create_default_config()
    
    def _create_default_config(self):
        """创建默认配置"""
        default_config = {
            'whitelist': [
                '文件传输助手',
                'SAYELF',
                'nicola king',
            ],
            'blacklist': [
                '广告群',
                '营销号',
            ],
            'patterns': [
                r'^测试',  # 以"测试"开头的消息
                r'.*HELP.*',  # 包含"HELP"的消息
            ],
            'enable_whitelist': True,  # 启用白名单
            'enable_blacklist': True,  # 启用黑名单
            'enable_pattern': True,  # 启用正则匹配
        }
        
        # 确保目录存在
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 保存配置
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ 创建默认配置：{self.config_file}")
        
        # 重新加载
        self.load_config()
    
    def should_process(self, sender: str, message: str) -> bool:
        """判断是否处理消息"""
        # 记录过滤日志
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'sender': sender,
            'message': message[:100],  # 只记录前 100 字
            'allowed': False,
            'reason': ''
        }
        
        # 1. 检查黑名单
        if self._in_blacklist(sender):
            log_entry['reason'] = '黑名单'
            self.filter_log.append(log_entry)
            logger.info(f"⛔ 黑名单拦截：{sender}")
            return False
        
        # 2. 检查白名单
        if self._in_whitelist(sender):
            log_entry['allowed'] = True
            log_entry['reason'] = '白名单'
            self.filter_log.append(log_entry)
            logger.info(f"✅ 白名单允许：{sender}")
            return True
        
        # 3. 检查正则匹配
        if self._match_pattern(message):
            log_entry['allowed'] = True
            log_entry['reason'] = '正则匹配'
            self.filter_log.append(log_entry)
            logger.info(f"✅ 正则匹配允许：{message[:50]}")
            return True
        
        # 4. 默认拒绝
        log_entry['reason'] = '不在白名单'
        self.filter_log.append(log_entry)
        logger.info(f"⛔ 默认拦截：{sender}")
        return False
    
    def _in_whitelist(self, sender: str) -> bool:
        """检查是否在白名单"""
        # 精确匹配
        if sender in self.whitelist:
            return True
        
        # 模糊匹配 (包含)
        for item in self.whitelist:
            if item in sender:
                return True
        
        return False
    
    def _in_blacklist(self, sender: str) -> bool:
        """检查是否在黑名单"""
        # 精确匹配
        if sender in self.blacklist:
            return True
        
        # 模糊匹配 (包含)
        for item in self.blacklist:
            if item in sender:
                return True
        
        return False
    
    def _match_pattern(self, message: str) -> bool:
        """检查是否匹配正则"""
        for pattern in self.patterns:
            if pattern.search(message):
                return True
        return False
    
    def add_to_whitelist(self, sender: str):
        """添加到白名单"""
        self.whitelist.add(sender)
        self._save_config()
        logger.info(f"✅ 添加到白名单：{sender}")
    
    def add_to_blacklist(self, sender: str):
        """添加到黑名单"""
        self.blacklist.add(sender)
        self._save_config()
        logger.info(f"✅ 添加到黑名单：{sender}")
    
    def _save_config(self):
        """保存配置"""
        config = {
            'whitelist': list(self.whitelist),
            'blacklist': list(self.blacklist),
            'patterns': [p.pattern for p in self.patterns],
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        total = len(self.filter_log)
        allowed = sum(1 for log in self.filter_log if log['allowed'])
        blocked = total - allowed
        
        return {
            'total_messages': total,
            'allowed': allowed,
            'blocked': blocked,
            'allow_rate': f"{allowed/total*100:.1f}%" if total > 0 else "0%",
            'whitelist_size': len(self.whitelist),
            'blacklist_size': len(self.blacklist),
        }


# 全局实例
whitelist_filter = WechatWhitelistFilter()


def main():
    """测试"""
    print("🧪 测试白名单过滤器...")
    
    # 测试消息
    test_messages = [
        ('文件传输助手', '你好'),
        ('SAYELF', '今天天气如何'),
        ('广告群', '优惠活动'),
        ('未知联系人', 'HELP'),
        ('未知联系人 2', '普通消息'),
    ]
    
    print("\n📊 测试结果:")
    for sender, message in test_messages:
        allowed = whitelist_filter.should_process(sender, message)
        status = "✅ 允许" if allowed else "⛔ 拦截"
        print(f"  {status}: {sender} - {message}")
    
    # 统计
    stats = whitelist_filter.get_stats()
    print(f"\n📈 统计:")
    print(f"  总消息：{stats['total_messages']}")
    print(f"  允许：{stats['allowed']}")
    print(f"  拦截：{stats['blocked']}")
    print(f"  通过率：{stats['allow_rate']}")
    
    print("\n✅ 测试完成！")


if __name__ == '__main__':
    main()
