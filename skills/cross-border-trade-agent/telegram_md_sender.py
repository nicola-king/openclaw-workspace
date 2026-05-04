#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram MD 文件发送优化 - 确保可点击打开
太一 AGI · 2026-04-19 11:21
"""

import logging
from pathlib import Path

logger = logging.getLogger('TelegramMDSender')

WORKSPACE = Path("/home/sayelf/.openclaw/workspace")


def check_telegram_compatibility(md_file_path: str) -> dict:
    """检查 MD 文件 Telegram 兼容性"""
    
    result = {
        "file_path": md_file_path,
        "exists": False,
        "readable": False,
        "encoding": "unknown",
        "size": 0,
        "size_formatted": "0 B",
        "telegram_compatible": False,
        "issues": [],
        "recommendations": []
    }
    
    # 检查文件存在
    file_path = Path(md_file_path)
    if not file_path.exists():
        result["issues"].append("❌ 文件不存在")
        result["recommendations"].append("检查文件路径是否正确")
        return result
    
    result["exists"] = True
    
    # 检查文件可读性和编码
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        result["readable"] = True
        result["encoding"] = "UTF-8"
    except UnicodeDecodeError:
        result["issues"].append("❌ 文件编码不是 UTF-8")
        result["recommendations"].append("使用 UTF-8 编码保存文件")
        return result
    except Exception as e:
        result["issues"].append(f"❌ 文件不可读：{str(e)}")
        return result
    
    # 计算文件大小
    result["size"] = file_path.stat().st_size
    
    # 格式化大小
    if result["size"] < 1024:
        result["size_formatted"] = f"{result['size']} B"
    elif result["size"] < 1024 * 1024:
        result["size_formatted"] = f"{result['size']/1024:.1f} KB"
    else:
        result["size_formatted"] = f"{result['size']/(1024*1024):.1f} MB"
    
    # Telegram 限制检查
    if result["size"] > 50 * 1024 * 1024:
        result["issues"].append("❌ 文件超过 Telegram 50MB 限制")
        result["recommendations"].append("压缩文件或分开发送")
    else:
        result["telegram_compatible"] = True
    
    # MD 格式检查
    if file_path.suffix.lower() != '.md':
        result["issues"].append("⚠️ 文件不是.md 格式")
        result["recommendations"].append("使用.md 扩展名")
    
    # 内容检查
    if len(content.strip()) == 0:
        result["issues"].append("❌ 文件内容为空")
        result["recommendations"].append("添加内容到文件")
    
    # Telegram 预览优化建议
    if result["size"] > 100 * 1024:
        result["recommendations"].append("💡 文件较大，考虑简化内容以提升 Telegram 预览体验")
    
    # 文件名检查
    filename = file_path.name
    if len(filename) > 100:
        result["issues"].append("⚠️ 文件名过长")
        result["recommendations"].append("使用简洁的文件名 (<100 字符)")
    
    # 特殊字符检查
    if any(c in filename for c in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']):
        result["issues"].append("⚠️ 文件名包含特殊字符")
        result["recommendations"].append("避免使用特殊字符")
    
    return result


def generate_telegram_friendly_md(content: str, title: str = "报告") -> str:
    """生成 Telegram 友好的 MD 内容"""
    
    from datetime import datetime
    
    # Telegram 友好的 MD 格式
    telegram_md = f"""# {title}

> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

{content}

---

*太一 AGI · {datetime.now().strftime('%Y-%m-%d')}*
"""
    
    return telegram_md


def main():
    """主函数 - 检查今日发送的 MD 文件"""
    logger.info("=" * 60)
    logger.info("📱 Telegram MD 文件兼容性检查")
    logger.info("=" * 60)
    
    # 今日发送的 MD 文件
    today_files = [
        "/home/sayelf/.openclaw/workspace/reports/7 大数据源验证模块集成报告_2026-04-19.md",
        "/home/sayelf/.openclaw/workspace/reports/全球产品趋势跟踪分析报告_2026-04-19.md",
        "/home/sayelf/.openclaw/workspace/reports/医疗器械_变压器_3D 打印机_市场调研报告.md",
        "/home/sayelf/.openclaw/workspace/reports/便携式储能电源_国内前 10 厂家分析.md"
    ]
    
    logger.info("\n📄 检查今日发送的 MD 文件:\n")
    
    compatible_count = 0
    
    for file_path in today_files:
        result = check_telegram_compatibility(file_path)
        
        logger.info(f"文件：{Path(file_path).name}")
        logger.info(f"  存在：{'✅' if result['exists'] else '❌'}")
        logger.info(f"  可读：{'✅' if result['readable'] else '❌'}")
        logger.info(f"  编码：{result['encoding']}")
        logger.info(f"  大小：{result['size_formatted']}")
        logger.info(f"  Telegram 兼容：{'✅' if result['telegram_compatible'] else '❌'}")
        
        if result["telegram_compatible"]:
            compatible_count += 1
        
        if result["issues"]:
            logger.info(f"  问题:")
            for issue in result["issues"]:
                logger.info(f"    {issue}")
        
        if result["recommendations"]:
            logger.info(f"  建议:")
            for rec in result["recommendations"]:
                logger.info(f"    {rec}")
        
        logger.info("")
    
    logger.info("=" * 60)
    logger.info(f"兼容性统计：{compatible_count}/{len(today_files)} 文件兼容")
    logger.info("✅ 检查完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
