#!/usr/bin/env python3
"""
Web-Check Python API 包装器 — 供智能代理系统自动化调用
"""
import json, os, sys, subprocess, time
from urllib.request import Request, urlopen
from urllib.error import URLError
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = SKILL_DIR / "repo"
SERVER_URL = "http://localhost:3001"


class WebCheck:
    """Web-Check 自动化调用器"""
    
    def __init__(self, base_url: str = SERVER_URL, auto_start: bool = True):
        self.base_url = base_url.rstrip("/")
        if auto_start:
            self._ensure_running()
    
    def _ensure_running(self):
        """确保服务运行，没跑就启动"""
        if self._health():
            return
        print("[web-check] ⚠️ 服务未运行，启动中...")
        subprocess.Popen(
            ["node", "server.js"],
            cwd=str(REPO_DIR),
            env={**os.environ, "PORT": "3001", "WC_SERVER": "true"},
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        for i in range(10):
            time.sleep(1.5)
            if self._health():
                print("[web-check] ✅ 服务已启动")
                return
        print("[web-check] ⚠️ 启动超时，尝试调用")
    
    def _health(self) -> bool:
        try:
            req = Request(f"{self.base_url}/api/get-ip?url=example.com")
            res = json.loads(urlopen(req, timeout=5).read().decode())
            return "ip" in res
        except:
            return False
    
    def _call(self, endpoint: str, url: str) -> dict:
        try:
            req = Request(f"{self.base_url}/api/{endpoint}?url={url}",
                          headers={"User-Agent": "Taiyi/1.0"})
            resp = urlopen(req, timeout=30)
            return json.loads(resp.read().decode())
        except Exception as e:
            return {"error": str(e), "endpoint": endpoint, "url": url}
    
    def ip_info(self, host: str) -> dict:
        return self._call("get-ip", host)
    
    def dns(self, host: str) -> dict:
        return self._call("dns", host)
    
    def ssl(self, host: str) -> dict:
        return self._call("ssl", host)
    
    def headers(self, host: str) -> dict:
        return self._call("headers", host)
    
    def ports(self, host: str) -> dict:
        return self._call("ports", host)
    
    def tech_stack(self, host: str) -> dict:
        return self._call("tech-stack", host)
    
    def cookies(self, host: str) -> dict:
        return self._call("cookies", host)
    
    def location(self, host: str) -> dict:
        return self._call("location", host)
    
    def http_security(self, host: str) -> dict:
        return self._call("http-security", host)
    
    def redirects(self, host: str) -> dict:
        return self._call("redirects", host)
    
    def subdomains(self, host: str) -> dict:
        return self._call("subdomains", host)
    
    def screenshot(self, host: str) -> str:
        return f"{self.base_url}/api/screenshot?host={host}"
    
    def carbon(self, host: str) -> dict:
        return self._call("carbon", host)
    
    def linked_pages(self, host: str) -> dict:
        return self._call("linked-pages", host)
    
    def security_txt(self, host: str) -> dict:
        return self._call("security-txt", host)
    
    def robots_txt(self, host: str) -> dict:
        return self._call("robots-txt", host)
    
    def analyze(self, host: str, modules: list = None) -> dict:
        """完整分析或指定模块"""
        all_modules = {
            "ip": self.ip_info,
            "dns": self.dns,
            "ssl": self.ssl,
            "headers": self.headers,
            "ports": self.ports,
            "tech": self.tech_stack,
            "cookies": self.cookies,
            "location": self.location,
            "security": self.http_security,
            "redirects": self.redirects,
            "subdomains": self.subdomains,
            "carbon": self.carbon,
        }
        targets = {k: v for k, v in all_modules.items() if modules is None or k in modules}
        results = {}
        for name, func in targets.items():
            try:
                results[name] = func(host)
            except Exception as e:
                results[name] = {"error": str(e)}
        return {"host": host, "results": results}
    
    def summarize(self, host: str) -> dict:
        """智能摘要 — 提取关键安全/技术信息"""
        full = self.analyze(host, ["ip", "dns", "ssl", "tech", "headers", "ports"])
        summary = {"host": host, "summary": {}}
        
        ip_data = full.get("results", {}).get("ip", {})
        if ip_data and "ip" in ip_data:
            summary["summary"]["ip"] = ip_data.get("ip")
            summary["summary"]["isp"] = ip_data.get("isp", ip_data.get("org", ""))
            summary["summary"]["country"] = ip_data.get("country", ip_data.get("location", ""))
        
        tech = full.get("results", {}).get("tech", {})
        if tech:
            summary["summary"]["tech_stack"] = list(tech.keys())[:10] if isinstance(tech, dict) else []
        
        ssl_data = full.get("results", {}).get("ssl", {})
        if ssl_data:
            summary["summary"]["ssl_valid"] = ssl_data.get("valid", ssl_data.get("issuer", "") != "")
            summary["summary"]["ssl_issuer"] = ssl_data.get("issuer", "")
        
        dns_data = full.get("results", {}).get("dns", {})
        if dns_data:
            has_mx = bool(dns_data.get("mx", []))
            has_spf = bool(dns_data.get("spf", False))
            has_dkim = bool(dns_data.get("dkim", False))
            summary["summary"]["email_security"] = {
                "mx": has_mx, "spf": has_spf, "dkim": has_dkim
            }
        
        ports_data = full.get("results", {}).get("ports", {})
        if ports_data:
            open_ports = ports_data.get("open", [])
            if not open_ports and isinstance(ports_data, list):
                open_ports = [p for p in ports_data if p.get("state") == "open"]
            summary["summary"]["open_ports"] = len(open_ports)
        
        return summary


# ── CLI ──
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Web-Check 网站分析")
    parser.add_argument("host", help="目标域名")
    parser.add_argument("-m", "--module", help="分析模块 (默认: summarize)", default="summarize")
    parser.add_argument("-j", "--json", help="原始 JSON 输出", action="store_true")
    args = parser.parse_args()
    
    wc = WebCheck()
    
    if args.module == "summarize":
        result = wc.summarize(args.host)
    elif args.module == "all":
        result = wc.analyze(args.host)
    else:
        func = getattr(wc, args.module, None)
        if func:
            result = func(args.host)
        else:
            print(f"未知模块: {args.module}")
            print(f"可用: summarize, all, ip, dns, ssl, headers, ports, tech, cookies, location, security, subdomains")
            sys.exit(1)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'='*50}")
        print(f"🔍 Web-Check 分析: {args.host}")
        print(f"{'='*50}")
        if isinstance(result, dict):
            if "summary" in result:
                s = result["summary"]
                print(f"IP: {s.get('ip','N/A')} ({s.get('country','')})")
                print(f"ISP: {s.get('isp','N/A')}")
                print(f"SSL: {'✅' if s.get('ssl_valid') else '❌'}")
                if s.get('ssl_issuer'): print(f"SSL Issuer: {s['ssl_issuer']}")
                print(f"Tech: {', '.join(s.get('tech_stack',['N/A'])[:8])}")
                if s.get('email_security'):
                    es = s['email_security']
                    print(f"Email Security: MX={'✅' if es.get('mx') else '❌'} SPF={'✅' if es.get('spf') else '❌'} DKIM={'✅' if es.get('dkim') else '❌'}")
                print(f"Open Ports: {s.get('open_ports','N/A')}")
            elif "results" in result:
                print(f"完整分析 ({len(result['results'])} 模块)")
            else:
                print(json.dumps(result, ensure_ascii=False, indent=2)[:500])
        print()
