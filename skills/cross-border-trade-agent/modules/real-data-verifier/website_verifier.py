#!/usr/bin/env python3
"""
跨境贸易 Agent - 智能网站验证模块
功能：验证客户网站真实性、邮箱有效性、需求数据匹配
"""

import requests
import re
import json
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

class WebsiteVerifier:
    """智能网站验证器"""
    
    def __init__(self):
        self.workspace = Path("/home/nicola/.openclaw/workspace")
        self.output_dir = self.workspace / "website-verification"
        self.output_dir.mkdir(exist_ok=True)
        
        # 邮箱正则
        self.email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        # 产品关键词
        self.product_keywords = {
            'generator': ['generator', 'generating set', 'genset', 'diesel generator', 'petrol generator'],
            'engine': ['engine', 'motor', 'gasoline engine', 'diesel engine'],
            'pump': ['pump', 'water pump', 'pumps'],
            'power': ['power', 'power solution', 'power equipment'],
        }
    
    def verify_website(self, url):
        """验证网站可访问性"""
        print(f"🔍 验证网站：{url}")
        
        try:
            response = requests.get(url, timeout=10)
            
            result = {
                'url': url,
                'status_code': response.status_code,
                'accessible': response.status_code == 200,
                'response_time': response.elapsed.total_seconds(),
                'content_type': response.headers.get('Content-Type', ''),
            }
            
            if response.status_code == 200:
                result['content'] = response.text[:50000]  # 保存部分内容用于分析
            else:
                result['content'] = ''
            
            return result
            
        except requests.exceptions.Timeout:
            return {'url': url, 'accessible': False, 'error': 'Timeout'}
        except requests.exceptions.ConnectionError:
            return {'url': url, 'accessible': False, 'error': 'Connection Error'}
        except Exception as e:
            return {'url': url, 'accessible': False, 'error': str(e)}
    
    def extract_emails(self, content):
        """从网页内容提取邮箱"""
        emails = re.findall(self.email_pattern, content)
        # 去重
        unique_emails = list(set(emails))
        return unique_emails
    
    def verify_email_format(self, email):
        """验证邮箱格式"""
        if re.match(self.email_pattern, email):
            domain = email.split('@')[1]
            return {
                'email': email,
                'valid_format': True,
                'domain': domain,
            }
        return {'email': email, 'valid_format': False}
    
    def check_product_match(self, content, product_type):
        """检查网站内容是否匹配产品类型"""
        if not content:
            return {'matched': False, 'keywords_found': []}
        
        content_lower = content.lower()
        keywords = self.product_keywords.get(product_type.lower(), [])
        
        found_keywords = []
        for keyword in keywords:
            if keyword.lower() in content_lower:
                found_keywords.append(keyword)
        
        return {
            'matched': len(found_keywords) > 0,
            'keywords_found': found_keywords,
            'match_score': len(found_keywords) / len(keywords) if keywords else 0
        }
    
    def extract_contact_info(self, content):
        """提取联系信息"""
        contact_info = {
            'emails': self.extract_emails(content),
            'phones': [],
            'addresses': []
        }
        
        # 提取电话（简单模式）
        phone_pattern = r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\./0-9]*'
        phones = re.findall(phone_pattern, content[:10000])
        contact_info['phones'] = [p.strip() for p in phones if len(p) > 6][:5]
        
        # 提取地址（查找常见地址关键词）
        address_keywords = ['address', 'road', 'street', 'city', 'country', 'no.', 'building']
        lines = content[:10000].split('\n')
        for line in lines:
            if any(kw in line.lower() for kw in address_keywords):
                contact_info['addresses'].append(line.strip())
        
        contact_info['addresses'] = contact_info['addresses'][:3]
        
        return contact_info
    
    def verify_customer(self, customer_data):
        """完整验证客户信息"""
        print(f"\n🔍 验证客户：{customer_data.get('name', 'Unknown')}")
        
        result = {
            'name': customer_data.get('name', ''),
            'country': customer_data.get('country', ''),
            'website': customer_data.get('website', ''),
            'verification_time': datetime.now().isoformat(),
        }
        
        # 1. 验证网站可访问性
        website_result = self.verify_website(result['website'])
        result['website_status'] = website_result
        
        if not website_result.get('accessible', False):
            result['overall_status'] = '❌ 网站不可访问'
            result['reliability_score'] = 0
            return result
        
        # 2. 提取联系信息
        content = website_result.get('content', '')
        contact_info = self.extract_contact_info(content)
        result['contact_info'] = contact_info
        
        # 3. 验证邮箱
        if contact_info['emails']:
            email_verification = self.verify_email_format(contact_info['emails'][0])
            result['email_verification'] = email_verification
        else:
            result['email_verification'] = {'emails_found': False}
        
        # 4. 检查产品匹配
        product_type = customer_data.get('product_type', 'generator')
        product_match = self.check_product_match(content, product_type)
        result['product_match'] = product_match
        
        # 5. 检查需求数据/项目
        project_indicators = ['project', 'requirement', 'need', 'buy', 'purchase', 'inquiry', 'RFQ']
        has_project_info = any(indicator in content.lower() for indicator in project_indicators)
        result['has_project_info'] = has_project_info
        
        # 6. 计算可靠性评分
        score = 0
        if website_result.get('accessible'):
            score += 30
        if contact_info['emails']:
            score += 25
        if contact_info['phones']:
            score += 15
        if product_match['matched']:
            score += 20
        if has_project_info:
            score += 10
        
        result['reliability_score'] = score
        result['overall_status'] = self._get_status_label(score)
        
        return result
    
    def _get_status_label(self, score):
        """根据评分获取状态标签"""
        if score >= 80:
            return '✅ 高度可信'
        elif score >= 60:
            return '🟡 可信'
        elif score >= 40:
            return '⚠️ 需进一步核实'
        else:
            return '❌ 不可信'
    
    def batch_verify(self, customers):
        """批量验证客户"""
        print(f"📦 批量验证：{len(customers)} 个客户")
        
        results = []
        for i, customer in enumerate(customers, 1):
            print(f"\n[{i}/{len(customers)}] {customer.get('name', 'Unknown')}")
            result = self.verify_customer(customer)
            results.append(result)
        
        # 保存验证结果
        self._save_results(results)
        
        return results
    
    def _save_results(self, results):
        """保存验证结果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"verification_result_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 验证结果已保存：{output_file}")
        
        # 同时保存 Markdown 版本
        md_file = self.output_dir / f"verification_result_{timestamp}.md"
        self._save_markdown(results, md_file)
    
    def _save_markdown(self, results, filepath):
        """保存为 Markdown 格式"""
        md_content = "# 🌍 海外客户网站验证报告\n\n"
        md_content += f"> **验证时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # 统计
        total = len(results)
        accessible = sum(1 for r in results if r.get('website_status', {}).get('accessible', False))
        with_email = sum(1 for r in results if r.get('contact_info', {}).get('emails'))
        high_reliability = sum(1 for r in results if r.get('reliability_score', 0) >= 80)
        
        md_content += f"## 📊 验证统计\n\n"
        md_content += f"- 总客户数：{total}\n"
        md_content += f"- 网站可访问：{accessible} ({accessible/total*100:.1f}%)\n"
        md_content += f"- 有邮箱：{with_email} ({with_email/total*100:.1f}%)\n"
        md_content += f"- 高可靠性：{high_reliability} ({high_reliability/total*100:.1f}%)\n\n"
        
        md_content += "## 🔍 详细验证结果\n\n"
        
        for result in results:
            md_content += f"### {result.get('name', 'Unknown')} ({result.get('country', '')})\n\n"
            md_content += f"**网站**: {result.get('website', 'N/A')}\n\n"
            md_content += f"**状态**: {result.get('overall_status', 'Unknown')}\n\n"
            md_content += f"**可靠性评分**: {result.get('reliability_score', 0)}/100\n\n"
            
            if result.get('contact_info'):
                contact = result['contact_info']
                if contact.get('emails'):
                    md_content += f"**邮箱**: {', '.join(contact['emails'])}\n\n"
                if contact.get('phones'):
                    md_content += f"**电话**: {', '.join(contact['phones'][:3])}\n\n"
            
            if result.get('product_match'):
                match = result['product_match']
                if match.get('matched'):
                    md_content += f"**产品匹配**: ✅ 找到关键词：{', '.join(match['keywords_found'])}\n\n"
            
            md_content += "---\n\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"📄 Markdown 报告已保存：{filepath}")


def main():
    """主函数 - 测试示例"""
    verifier = WebsiteVerifier()
    
    # 测试客户数据
    test_customers = [
        {
            'name': 'Siam Power Co., Ltd',
            'country': 'Thailand',
            'website': 'https://www.siampower.co.th',
            'product_type': 'generator'
        },
        {
            'name': 'Dubai Generator LLC',
            'country': 'UAE',
            'website': 'https://dubaigenerator.com',
            'product_type': 'generator'
        },
        {
            'name': 'Dembal Generators',
            'country': 'Nigeria',
            'website': 'https://dembalgenerators.com',
            'product_type': 'generator'
        }
    ]
    
    results = verifier.batch_verify(test_customers)
    
    print(f"\n🎉 验证完成！")
    print(f"总客户数：{len(results)}")
    print(f"高可靠性：{sum(1 for r in results if r.get('reliability_score', 0) >= 80)}")


if __name__ == "__main__":
    main()
