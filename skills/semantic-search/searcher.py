#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Semantic Searcher - FTS5 搜索执行器

版本：v1.0 | 创建：2026-04-08
功能：执行语义搜索，返回相关性排序结果
"""

import sqlite3
import re
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class SemanticSearcher:
    """语义搜索执行器"""
    
    def __init__(self, db_path: str = '/home/nicola/.openclaw/workspace/skills/semantic-search/db/semantic_index.db'):
        self.db_path = Path(db_path)
        self.conn = None
        self._connect()
    
    def _connect(self):
        """连接数据库"""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
    
    def search(self, query: str, filters: Optional[Dict] = None) -> List[Dict]:
        """执行搜索"""
        # 解析查询
        parsed = self._parse_query(query)
        
        # 合并过滤器
        if filters:
            parsed['filters'].update(filters)
        
        # 执行搜索
        results = []
        
        # 确定搜索范围
        search_types = parsed['filters'].get('type', ['memory', 'skill', 'constitution'])
        
        for search_type in search_types:
            type_results = self._search_type(search_type, parsed['keywords'], parsed['filters'])
            results.extend(type_results)
        
        # 排序
        results = self._rank_results(results, parsed['keywords'])
        
        # 记录搜索历史
        self._log_search(query, len(results))
        
        return results
    
    def _parse_query(self, query: str) -> Dict:
        """解析查询字符串"""
        keywords = []
        filters = {}
        
        # 解析 type: 过滤器
        type_matches = re.findall(r'type:(\w+)', query)
        if type_matches:
            filters['type'] = type_matches
            query = re.sub(r'type:\w+\s*', '', query)
        
        # 解析 tag: 过滤器
        tag_matches = re.findall(r'tag:(\w+)', query)
        if tag_matches:
            filters['tags'] = tag_matches
            query = re.sub(r'tag:\w+\s*', '', query)
        
        # 解析时间范围
        date_range = self._parse_date_range(query)
        if date_range:
            filters['date_range'] = date_range
            query = re.sub(r'\d{4}-\d{2}-\d{2}[\.\.~]\d{4}-\d{2}-\d{2}\s*', '', query)
            query = re.sub(r'last:\d+d\s*', '', query)
        
        # 解析布尔逻辑
        if ' AND ' in query:
            filters['boolean'] = 'AND'
            query = query.replace(' AND ', ' ')
        elif ' OR ' in query:
            filters['boolean'] = 'OR'
            query = query.replace(' OR ', ' ')
        elif ' NOT ' in query:
            filters['boolean'] = 'NOT'
            query = query.replace(' NOT ', ' -')
        
        # 提取短语搜索
        phrase_matches = re.findall(r'"([^"]+)"', query)
        if phrase_matches:
            filters['phrases'] = phrase_matches
            query = re.sub(r'"[^"]+"\s*', '', query)
        
        # 剩余部分作为关键词
        keywords = query.strip().split()
        
        return {
            'keywords': keywords,
            'filters': filters
        }
    
    def _parse_date_range(self, query: str) -> Optional[Tuple[str, str]]:
        """解析时间范围"""
        # 格式 1: 2026-04-01..2026-04-08
        range_match = re.search(r'(\d{4}-\d{2}-\d{2})[\.\.~](\d{4}-\d{2}-\d{2})', query)
        if range_match:
            return (range_match.group(1), range_match.group(2))
        
        # 格式 2: last:7d
        last_match = re.search(r'last:(\d+)d', query)
        if last_match:
            days = int(last_match.group(1))
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            return (start_date, end_date)
        
        return None
    
    def _search_type(self, search_type: str, keywords: List[str], filters: Dict) -> List[Dict]:
        """在指定类型中搜索"""
        cursor = self.conn.cursor()
        
        # 确定索引表
        table_map = {
            'memory': 'memory_index',
            'skill': 'skill_index',
            'constitution': 'constitution_index',
            'conversation': 'conversation_index'
        }
        
        table = table_map.get(search_type, 'memory_index')
        
        # 构建查询
        if keywords:
            # FTS5 查询
            query_text = ' '.join(keywords)
            if filters.get('boolean') == 'AND':
                query_text = ' AND '.join(keywords)
            elif filters.get('boolean') == 'OR':
                query_text = ' OR '.join(keywords)
            
            # 短语搜索
            if 'phrases' in filters:
                for phrase in filters['phrases']:
                    query_text += f' "{phrase}"'
            
            sql = f'''
                SELECT *, bm25({table}) as rank
                FROM {table}
                WHERE {table} MATCH ?
            '''
            params = [query_text]
        else:
            sql = f'SELECT *, 0 as rank FROM {table}'
            params = []
        
        # 添加过滤器
        if 'date_range' in filters:
            sql += ' AND date BETWEEN ? AND ?'
            params.extend(filters['date_range'])
        
        if 'tags' in filters:
            for tag in filters['tags']:
                sql += ' AND tags LIKE ?'
                params.append(f'%{tag}%')
        
        sql += ' ORDER BY rank'
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    def _rank_results(self, results: List[Dict], keywords: List[str]) -> List[Dict]:
        """对结果排序"""
        for result in results:
            # FTS5 排名
            fts5_rank = -result.get('rank', 0)
            
            # 关键词匹配度
            keyword_score = self._keyword_match_score(result, keywords)
            
            # 时间新鲜度
            recency_score = self._recency_score(result.get('date', ''))
            
            # 综合评分
            result['relevance'] = (
                0.5 * self._normalize(fts5_rank, 0, 10) +
                0.3 * keyword_score +
                0.2 * recency_score
            )
        
        # 按相关性排序
        results.sort(key=lambda x: x['relevance'], reverse=True)
        
        return results
    
    def _keyword_match_score(self, result: Dict, keywords: List[str]) -> float:
        """计算关键词匹配度"""
        if not keywords:
            return 0
        
        content = result.get('content', '') + result.get('title', '')
        matches = sum(1 for kw in keywords if kw.lower() in content.lower())
        return matches / len(keywords)
    
    def _recency_score(self, date_str: str) -> float:
        """计算时间新鲜度"""
        if not date_str or date_str == 'unknown':
            return 0.5
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            days_old = (datetime.now() - date).days
            # 7 天内满分，每过 7 天减半
            score = max(0, 1.0 - (days_old / 30))
            return score
        except:
            return 0.5
    
    def _normalize(self, value: float, min_val: float, max_val: float) -> float:
        """归一化"""
        if max_val == min_val:
            return 0.5
        return max(0, min(1, (value - min_val) / (max_val - min_val)))
    
    def _log_search(self, query: str, results_count: int):
        """记录搜索历史"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO search_history (query, timestamp, results_count)
            VALUES (?, ?, ?)
        ''', (query, datetime.now().isoformat(), results_count))
        self.conn.commit()
    
    def generate_summary(self, results: List[Dict], query: str) -> str:
        """为搜索结果生成摘要"""
        if not results:
            return f"未找到与「{query}」相关的内容"
        
        # 提取前 3 个结果
        top_results = results[:3]
        
        summary_lines = [
            f"📊 找到 {len(results)} 个相关文件：",
            ""
        ]
        
        for i, result in enumerate(top_results, 1):
            title = result.get('title', result.get('name', '未知'))
            file_path = result.get('file_path', '')
            relevance = result.get('relevance', 0)
            
            summary_lines.append(
                f"{i}. **{title}** (相关性：{relevance:.2f})\n   `{file_path}`"
            )
        
        return '\n'.join(summary_lines)
    
    def get_related(self, results: List[Dict]) -> Dict:
        """获取相关内容推荐"""
        if not results:
            return {}
        
        # 基于标签相似
        tags = set()
        for result in results:
            tag_str = result.get('tags', '')
            tags.update(tag_str.split())
        
        return {
            'tags': list(tags)[:5],
            'types': list(set(r.get('type', 'unknown') for r in results))
        }
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()


# 使用示例
if __name__ == '__main__':
    searcher = SemanticSearcher()
    
    # 示例搜索
    results = searcher.search("hermes 技能")
    print(searcher.generate_summary(results, "hermes 技能"))
    
    searcher.close()
