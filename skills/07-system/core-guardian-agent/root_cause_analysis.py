#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
故障根因分析模块 - Core Guardian Agent v3.0

功能:
- 5 Why 分析法
- 自动定位根因
- 生成解决方案

作者：太一 AGI
创建：2026-04-12 22:56
版本：v1.0
"""

from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger('RootCauseAnalysis')


class RootCauseAnalysis:
    """故障根因分析"""
    
    def __init__(self):
        """初始化根因分析"""
        self.why_chain = []
        self.common_causes = {
            'Gateway 端口未监听': [
                '端口被占用',
                'Gateway 进程崩溃',
                '配置文件错误',
                '系统资源不足',
            ],
            'CPU 使用率过高': [
                '进程泄漏',
                '高负载任务',
                '系统更新',
                '恶意软件',
            ],
            '内存使用率过高': [
                '内存泄漏',
                '缓存未清理',
                '进程过多',
                '配置不当',
            ],
            '磁盘使用率过高': [
                '日志文件过大',
                '临时文件未清理',
                '数据备份过多',
                '用户文件过多',
            ],
        }
        
        logger.info("🔍 故障根因分析模块已初始化")
    
    def analyze(self, problem: str, symptoms: List[str]) -> Dict:
        """分析故障根因"""
        logger.info(f"🔍 分析故障：{problem}")
        
        # 5 Why 分析
        self.why_chain = self.five_whys(problem, symptoms)
        
        # 匹配常见原因
        matched_causes = self.match_common_causes(problem, symptoms)
        
        # 生成解决方案
        solutions = self.generate_solutions(problem, self.why_chain, matched_causes)
        
        result = {
            'problem': problem,
            'symptoms': symptoms,
            'why_chain': self.why_chain,
            'root_causes': matched_causes,
            'solutions': solutions,
            'confidence': self.calculate_confidence(matched_causes),
            'timestamp': datetime.now().isoformat(),
        }
        
        logger.info(f"✅ 根因分析完成：{len(self.why_chain)} 个 Why, {len(matched_causes)} 个根因")
        
        return result
    
    def five_whys(self, problem: str, symptoms: List[str]) -> List[Dict]:
        """5 Why 分析法"""
        why_chain = []
        
        # Why 1: 为什么出现问题？
        why_1 = f"为什么 {problem}？"
        answer_1 = self.get_answer(problem, symptoms, level=1)
        why_chain.append({'why': why_1, 'answer': answer_1})
        
        # Why 2: 为什么会出现这个原因？
        why_2 = f"为什么 {answer_1}？"
        answer_2 = self.get_answer(answer_1, symptoms, level=2)
        why_chain.append({'why': why_2, 'answer': answer_2})
        
        # Why 3: 为什么会出现这个深层原因？
        why_3 = f"为什么 {answer_2}？"
        answer_3 = self.get_answer(answer_2, symptoms, level=3)
        why_chain.append({'why': why_3, 'answer': answer_3})
        
        # Why 4: 为什么会出现这个根本原因？
        why_4 = f"为什么 {answer_3}？"
        answer_4 = self.get_answer(answer_3, symptoms, level=4)
        why_chain.append({'why': why_4, 'answer': answer_4})
        
        # Why 5: 为什么会出现这个系统性原因？
        why_5 = f"为什么 {answer_4}？"
        answer_5 = self.get_answer(answer_4, symptoms, level=5)
        why_chain.append({'why': why_5, 'answer': answer_5})
        
        logger.info(f"📝 5 Why 分析完成")
        for i, item in enumerate(why_chain, 1):
            logger.info(f"  Why{i}: {item['why']}")
            logger.info(f"       → {item['answer']}")
        
        return why_chain
    
    def get_answer(self, question: str, symptoms: List[str], level: int) -> str:
        """获取 Why 的答案"""
        # 基于问题类型和症状生成答案
        if 'Gateway' in question or '端口' in question:
            answers = [
                'Gateway 进程异常',
                '系统资源不足',
                '配置错误',
                '系统更新导致',
                '系统架构问题',
            ]
        elif 'CPU' in question:
            answers = [
                '进程占用过高',
                '系统负载过高',
                '配置不当',
                '硬件性能不足',
                '系统架构问题',
            ]
        elif '内存' in question:
            answers = [
                '内存泄漏',
                '缓存未清理',
                '配置不当',
                '硬件资源不足',
                '系统架构问题',
            ]
        elif '磁盘' in question:
            answers = [
                '日志文件过大',
                '临时文件过多',
                '配置不当',
                '存储规划不足',
                '系统架构问题',
            ]
        else:
            answers = [
                '系统异常',
                '资源不足',
                '配置错误',
                '维护不足',
                '系统架构问题',
            ]
        
        # 根据层级选择答案
        index = min(level - 1, len(answers) - 1)
        return answers[index]
    
    def match_common_causes(self, problem: str, symptoms: List[str]) -> List[Dict]:
        """匹配常见原因"""
        matched = []
        
        # 查找匹配的问题类型
        for key, causes in self.common_causes.items():
            if key in problem or any(symptom in problem for symptom in key.split()):
                for cause in causes:
                    matched.append({
                        'cause': cause,
                        'category': key,
                        'probability': self.calculate_probability(cause, symptoms),
                    })
        
        # 按概率排序
        matched.sort(key=lambda x: x['probability'], reverse=True)
        
        return matched[:5]  # 返回前 5 个
    
    def calculate_probability(self, cause: str, symptoms: List[str]) -> float:
        """计算概率"""
        # 简单概率计算
        base_probability = 0.5
        
        # 根据症状调整
        if '频繁' in str(symptoms):
            base_probability += 0.2
        if '突然' in str(symptoms):
            base_probability += 0.1
        
        return min(base_probability, 1.0)
    
    def generate_solutions(self, problem: str, why_chain: List[Dict], root_causes: List[Dict]) -> List[Dict]:
        """生成解决方案"""
        solutions = []
        
        # 针对每个根因生成解决方案
        for root_cause in root_causes:
            cause = root_cause['cause']
            
            solution = {
                'cause': cause,
                'steps': self.get_solution_steps(cause),
                'commands': self.get_solution_commands(cause),
                'estimated_time': self.get_estimated_time(cause),
                'success_rate': root_cause['probability'],
            }
            solutions.append(solution)
        
        return solutions
    
    def get_solution_steps(self, cause: str) -> List[str]:
        """获取解决方案步骤"""
        steps_map = {
            '端口被占用': [
                '1. 检查端口占用情况',
                '2. 停止占用端口的进程',
                '3. 重启 Gateway',
                '4. 验证恢复',
            ],
            'Gateway 进程崩溃': [
                '1. 检查 Gateway 日志',
                '2. 分析崩溃原因',
                '3. 修复问题',
                '4. 重启 Gateway',
            ],
            '内存泄漏': [
                '1. 识别泄漏进程',
                '2. 停止泄漏进程',
                '3. 清理内存',
                '4. 更新/修复进程',
            ],
            '日志文件过大': [
                '1. 查找大日志文件',
                '2. 清理旧日志',
                '3. 配置日志轮转',
                '4. 监控磁盘空间',
            ],
        }
        
        return steps_map.get(cause, [
            '1. 分析问题',
            '2. 制定方案',
            '3. 执行修复',
            '4. 验证结果',
        ])
    
    def get_solution_commands(self, cause: str) -> List[str]:
        """获取解决方案命令"""
        commands_map = {
            '端口被占用': [
                'netstat -tln | grep 18789',
                'lsof -i :18789',
                'kill -9 <PID>',
                'systemctl restart openclaw-gateway',
            ],
            'Gateway 进程崩溃': [
                'journalctl -u openclaw-gateway -n 50',
                'cat /home/nicola/.openclaw/workspace/logs/gateway.log | tail -100',
                'systemctl restart openclaw-gateway',
            ],
            '内存泄漏': [
                'ps aux --sort=-%mem | head -10',
                'kill -9 <PID>',
                'sync; echo 3 > /proc/sys/vm/drop_caches',
            ],
            '日志文件过大': [
                'find /home/nicola/.openclaw/workspace/logs -type f -size +100M',
                'find /home/nicola/.openclaw/workspace/logs -type f -mtime +30 -delete',
                'df -h',
            ],
        }
        
        return commands_map.get(cause, [
            '# 通用命令',
            'systemctl status <service>',
            'journalctl -u <service> -n 50',
        ])
    
    def get_estimated_time(self, cause: str) -> int:
        """获取预计解决时间 (分钟)"""
        time_map = {
            '端口被占用': 5,
            'Gateway 进程崩溃': 10,
            '内存泄漏': 15,
            '日志文件过大': 10,
        }
        
        return time_map.get(cause, 15)
    
    def calculate_confidence(self, root_causes: List[Dict]) -> float:
        """计算置信度"""
        if not root_causes:
            return 0.0
        
        # 基于最高概率的根因计算置信度
        max_probability = max(rc['probability'] for rc in root_causes)
        
        # 基于 Why 链长度调整
        why_bonus = min(len(self.why_chain) / 5, 0.2)
        
        return min(max_probability + why_bonus, 1.0)


def main():
    """主函数 - 测试"""
    logger.info("🔍 故障根因分析模块测试...")
    
    rca = RootCauseAnalysis()
    
    # 测试 Gateway 问题
    problem = 'Gateway 端口未监听'
    symptoms = ['进程运行中', '端口未监听', '频繁发生']
    result = rca.analyze(problem, symptoms)
    
    logger.info(f"✅ 问题分析：{result['problem']}")
    logger.info(f"  根因数量：{len(result['root_causes'])}")
    logger.info(f"  置信度：{result['confidence']*100:.1f}%")
    logger.info(f"  解决方案：{len(result['solutions'])} 个")
    
    # 显示 5 Why 链
    logger.info(f"\n📝 5 Why 分析:")
    for i, item in enumerate(result['why_chain'], 1):
        logger.info(f"  Why{i}: {item['why']}")
        logger.info(f"       → {item['answer']}")
    
    # 显示根因
    logger.info(f"\n🔍 根因分析:")
    for rc in result['root_causes'][:3]:
        logger.info(f"  - {rc['cause']} (概率：{rc['probability']*100:.1f}%)")
    
    # 显示解决方案
    logger.info(f"\n💡 解决方案:")
    for sol in result['solutions'][:2]:
        logger.info(f"  根因：{sol['cause']}")
        logger.info(f"  预计时间：{sol['estimated_time']} 分钟")
        logger.info(f"  成功率：{sol['success_rate']*100:.1f}%")
    
    logger.info("\n✅ 故障根因分析模块测试完成！")


if __name__ == '__main__':
    main()
