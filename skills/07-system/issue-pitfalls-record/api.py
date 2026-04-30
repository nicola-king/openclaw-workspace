#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
踩坑记录 API - 问题与解决方案知识库

提供:
- 问题记录
- 解决方案查询
- 知识库管理
- 与 Core Guardian Agent 集成

作者：太一 AGI
创建：2026-04-12
版本：v1.0
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import logging

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('IssuePitfallsAPI')


@dataclass
class Issue:
    """问题记录"""
    issue_id: str
    timestamp: str
    severity: str  # P0/P1/P2/P3
    category: str  # gateway/ubuntu/taiyi/other
    title: str
    description: str
    root_cause: Optional[str] = None
    solution: Optional[str] = None
    status: str = 'open'  # open/resolved/closed
    resolved_at: Optional[str] = None
    tags: List[str] = None
    related_files: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.related_files is None:
            self.related_files = []


@dataclass
class Solution:
    """解决方案"""
    solution_id: str
    category: str
    problem: str
    steps: List[str]
    commands: List[str]
    success_rate: float = 0.0
    avg_time_minutes: float = 0.0
    last_used: Optional[str] = None
    usage_count: int = 0


class IssuePitfallsAPI:
    """踩坑记录 API"""
    
    def __init__(self):
        """初始化 API"""
        self.base_dir = Path('/home/nicola/.openclaw/workspace/skills/07-system/issue-pitfalls-record')
        self.issues_dir = self.base_dir / 'issues'
        self.solutions_dir = self.base_dir / 'solutions'
        self.knowledge_base_file = self.base_dir / 'knowledge_base.json'
        
        # 创建目录
        self.issues_dir.mkdir(parents=True, exist_ok=True)
        for severity in ['P0', 'P1', 'P2', 'P3']:
            (self.issues_dir / severity).mkdir(parents=True, exist_ok=True)
        
        self.solutions_dir.mkdir(parents=True, exist_ok=True)
        for category in ['gateway', 'ubuntu', 'taiyi', 'other']:
            (self.solutions_dir / category).mkdir(parents=True, exist_ok=True)
        
        # 加载知识库
        self.knowledge_base = self.load_knowledge_base()
        
        logger.info("📝 踩坑记录 API 已初始化")
        logger.info(f"  知识库：{len(self.knowledge_base.get('issues', []))} 个问题，{len(self.knowledge_base.get('solutions', []))} 个解决方案")
    
    def add_issue(self, issue: Issue) -> str:
        """添加问题记录"""
        logger.info(f"📝 添加问题记录：{issue.title}")
        
        # 生成 Issue ID
        if not issue.issue_id:
            issue_id = f"ISSUE-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
            issue.issue_id = issue_id
        
        # 保存到文件
        issue_file = self.issues_dir / issue.severity / f"{issue.issue_id}.json"
        with open(issue_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(issue), f, indent=2, ensure_ascii=False)
        
        # 更新知识库
        if 'issues' not in self.knowledge_base:
            self.knowledge_base['issues'] = []
        self.knowledge_base['issues'].append(asdict(issue))
        self.save_knowledge_base()
        
        logger.info(f"✅ 问题记录已保存：{issue_file}")
        
        return issue.issue_id
    
    def add_solution(self, solution: Solution) -> str:
        """添加解决方案"""
        logger.info(f"📝 添加解决方案：{solution.problem}")
        
        # 生成 Solution ID
        if not solution.solution_id:
            solution_id = f"SOL-{solution.category.upper()}-{uuid.uuid4().hex[:6].upper()}"
            solution.solution_id = solution_id
        
        # 保存到文件
        solution_file = self.solutions_dir / solution.category / f"{solution.solution_id}.json"
        with open(solution_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(solution), f, indent=2, ensure_ascii=False)
        
        # 更新知识库
        if 'solutions' not in self.knowledge_base:
            self.knowledge_base['solutions'] = []
        self.knowledge_base['solutions'].append(asdict(solution))
        self.save_knowledge_base()
        
        logger.info(f"✅ 解决方案已保存：{solution_file}")
        
        return solution.solution_id
    
    def search_issues(self, category: Optional[str] = None, severity: Optional[str] = None, status: Optional[str] = None) -> List[Dict]:
        """搜索问题记录"""
        logger.info(f"🔍 搜索问题记录：category={category}, severity={severity}, status={status}")
        
        issues = self.knowledge_base.get('issues', [])
        
        # 过滤
        if category:
            issues = [i for i in issues if i.get('category') == category]
        if severity:
            issues = [i for i in issues if i.get('severity') == severity]
        if status:
            issues = [i for i in issues if i.get('status') == status]
        
        logger.info(f"✅ 找到 {len(issues)} 个问题记录")
        
        return issues
    
    def search_solution(self, problem_keyword: str) -> Optional[Dict]:
        """搜索解决方案"""
        logger.info(f"🔍 搜索解决方案：{problem_keyword}")
        
        solutions = self.knowledge_base.get('solutions', [])
        
        # 关键词匹配
        matched_solutions = []
        for solution in solutions:
            if problem_keyword.lower() in solution.get('problem', '').lower():
                matched_solutions.append(solution)
        
        # 按成功率排序
        matched_solutions.sort(key=lambda x: x.get('success_rate', 0), reverse=True)
        
        if matched_solutions:
            logger.info(f"✅ 找到解决方案：{matched_solutions[0]['problem']} (成功率：{matched_solutions[0].get('success_rate', 0)*100:.1f}%)")
            return matched_solutions[0]
        else:
            logger.info(f"⚠️ 未找到匹配的解决方案")
            return None
    
    def resolve_issue(self, issue_id: str, solution: Optional[str] = None):
        """解决问题"""
        logger.info(f"🔧 解决问题：{issue_id}")
        
        # 查找问题
        issues = self.knowledge_base.get('issues', [])
        issue = None
        for i in issues:
            if i.get('issue_id') == issue_id:
                issue = i
                break
        
        if not issue:
            logger.error(f"❌ 问题未找到：{issue_id}")
            return
        
        # 更新状态
        issue['status'] = 'resolved'
        issue['resolved_at'] = datetime.now().isoformat()
        if solution:
            issue['solution'] = solution
        
        # 保存到文件
        issue_file = self.issues_dir / issue['severity'] / f"{issue_id}.json"
        if issue_file.exists():
            with open(issue_file, 'w', encoding='utf-8') as f:
                json.dump(issue, f, indent=2, ensure_ascii=False)
        
        # 更新知识库
        self.save_knowledge_base()
        
        logger.info(f"✅ 问题已解决：{issue_id}")
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        issues = self.knowledge_base.get('issues', [])
        solutions = self.knowledge_base.get('solutions', [])
        
        stats = {
            'total_issues': len(issues),
            'open_issues': len([i for i in issues if i.get('status') == 'open']),
            'resolved_issues': len([i for i in issues if i.get('status') == 'resolved']),
            'closed_issues': len([i for i in issues if i.get('status') == 'closed']),
            'total_solutions': len(solutions),
            'avg_success_rate': sum(s.get('success_rate', 0) for s in solutions) / len(solutions) if solutions else 0,
            'by_severity': {
                'P0': len([i for i in issues if i.get('severity') == 'P0']),
                'P1': len([i for i in issues if i.get('severity') == 'P1']),
                'P2': len([i for i in issues if i.get('severity') == 'P2']),
                'P3': len([i for i in issues if i.get('severity') == 'P3']),
            },
            'by_category': {},
        }
        
        # 按分类统计
        for issue in issues:
            category = issue.get('category', 'other')
            if category not in stats['by_category']:
                stats['by_category'][category] = 0
            stats['by_category'][category] += 1
        
        return stats
    
    def load_knowledge_base(self) -> Dict:
        """加载知识库"""
        if self.knowledge_base_file.exists():
            try:
                with open(self.knowledge_base_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"⚠️ 加载知识库失败：{e}")
                return {'issues': [], 'solutions': []}
        else:
            logger.info("  新建知识库")
            return {'issues': [], 'solutions': []}
    
    def save_knowledge_base(self):
        """保存知识库"""
        with open(self.knowledge_base_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ 知识库已保存：{self.knowledge_base_file}")
    
    def integrate_with_core_guardian(self, metrics):
        """与 Core Guardian Agent 集成"""
        logger.info("🔗 与 Core Guardian Agent 集成...")
        
        # 检测 Gateway 问题
        if metrics.gateway_running and not metrics.gateway_port_ok:
            issue = Issue(
                severity='P1',
                category='gateway',
                title='Gateway 端口未监听',
                description=f'Gateway 进程运行 (PID: {metrics.gateway_pid}) 但端口 18789 未监听',
                tags=['gateway', 'port', 'network'],
            )
            self.add_issue(issue)
            logger.info(f"📝 已记录问题：{issue.issue_id}")
        
        # 检测 CPU 过高
        if metrics.cpu_usage > 80:
            issue = Issue(
                severity='P2',
                category='ubuntu',
                title='CPU 使用率过高',
                description=f'CPU 使用率：{metrics.cpu_usage:.1f}%',
                tags=['cpu', 'performance', 'ubuntu'],
            )
            self.add_issue(issue)
            logger.info(f"📝 已记录问题：{issue.issue_id}")
        
        # 检测内存过高
        if metrics.memory_usage > 80:
            issue = Issue(
                severity='P2',
                category='ubuntu',
                title='内存使用率过高',
                description=f'内存使用率：{metrics.memory_usage:.1f}%',
                tags=['memory', 'performance', 'ubuntu'],
            )
            self.add_issue(issue)
            logger.info(f"📝 已记录问题：{issue.issue_id}")
        
        # 检测磁盘过高
        if metrics.disk_usage > 90:
            issue = Issue(
                severity='P2',
                category='ubuntu',
                title='磁盘使用率过高',
                description=f'磁盘使用率：{metrics.disk_usage:.1f}%',
                tags=['disk', 'storage', 'ubuntu'],
            )
            self.add_issue(issue)
            logger.info(f"📝 已记录问题：{issue.issue_id}")
        
        logger.info("✅ 与 Core Guardian Agent 集成完成")


def main():
    """主函数 - 测试"""
    logger.info("📝 踩坑记录 API 测试...")
    
    api = IssuePitfallsAPI()
    
    # 测试添加问题
    issue = Issue(
        issue_id='',
        timestamp=datetime.now().isoformat(),
        severity='P2',
        category='gateway',
        title='测试问题',
        description='这是一个测试问题记录',
        tags=['test'],
    )
    issue_id = api.add_issue(issue)
    logger.info(f"✅ 测试问题已添加：{issue_id}")
    
    # 测试添加解决方案
    solution = Solution(
        solution_id='',
        category='gateway',
        problem='Gateway 端口未监听',
        steps=[
            '1. 检查 Gateway 进程',
            '2. 检查端口占用',
            '3. 重启 Gateway',
            '4. 验证恢复',
        ],
        commands=[
            'pgrep -f openclaw-gateway',
            'netstat -tln | grep 18789',
            'systemctl restart openclaw-gateway',
        ],
        success_rate=0.95,
        avg_time_minutes=2,
    )
    solution_id = api.add_solution(solution)
    logger.info(f"✅ 测试解决方案已添加：{solution_id}")
    
    # 测试搜索
    matched = api.search_solution('Gateway 端口')
    if matched:
        logger.info(f"✅ 搜索成功：{matched['problem']}")
    
    # 测试统计
    stats = api.get_stats()
    logger.info(f"📊 统计信息：{stats}")
    
    logger.info("✅ 踩坑记录 API 测试完成！")


if __name__ == '__main__':
    main()
