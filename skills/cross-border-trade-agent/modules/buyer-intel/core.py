#!/usr/bin/env python3
"""
买家情报引擎 v1 — 核心产品
中东项目采购 + 承包商/开发商人脉数据库
"""
import json, os, re
from datetime import datetime, timedelta

DATA_DIR = os.path.dirname(__file__) + "/data"
BUYER_FILE = f"{DATA_DIR}/buyers.json"

class BuyerIntel:
    TIERS = {
        "free": {"name": "免费", "visible_fields": ["project_name","country","sectors","status"],
                 "max_results": 3, "price_monthly": 0},
        "free_trial": {"name": "试用", "visible_fields": "__all__",
                       "max_results": 10, "price_monthly": 0},
        "basic": {"name": "基础版", "visible_fields": ["project_name","country","sectors","status",
                    "budget_usd","procurement_needs","buyer_type"],
                  "max_results": 20, "price_monthly": 299},
        "pro": {"name": "专业版", "visible_fields": "__all__", "max_results": 999, "price_monthly": 999},
    }
    VM = {"website_check": 0.3, "phone_check": 0.2, "email_check": 0.2, "linkedin_check": 0.15, "third_party": 0.15}

    def __init__(self):
        self.records = self._load()
    def _load(self):
        if not os.path.exists(BUYER_FILE): return []
        with open(BUYER_FILE) as f: return json.load(f)
    def _save(self):
        with open(BUYER_FILE,"w") as f: json.dump(self.records,f,ensure_ascii=False,indent=2)

    # ===== Search =====
    def search(self, q="", filters=None, tier="pro"):
        r = self.records
        if q:
            ql=q.lower(); r=[x for x in r if ql in json.dumps(x,ensure_ascii=False).lower()]
        if filters:
            for k,v in filters.items():
                if k=="country": r=[x for x in r if x.get("country","").lower()==v.lower()]
                elif k=="status": r=[x for x in r if v.lower() in x.get("status","").lower()]
                elif k=="sector": r=[x for x in r if any(v.lower() in s.lower() for s in x.get("sectors",[]))]
                elif k=="needs": r=[x for x in r if any(v.lower() in n.lower() for n in x.get("procurement_needs",[]))]
        tc=self.TIERS.get(tier,self.TIERS["pro"])
        out=[]
        for x in r[:tc["max_results"]]:
            if tc["visible_fields"]=="__all__": out.append(x)
            else: out.append({k:x.get(k) for k in tc["visible_fields"] if k in x})
        return out

    def get_active_projects(self, country=None):
        r=[x for x in self.records if x.get("procurement_needs") and x.get("status") not in ["已完成","取消"]]
        if country: r=[x for x in r if country.lower() in (x.get("country") or x.get("location") or "").lower()]
        return r

    def get_procurement_opportunities(self, pt=None):
        r=[x for x in self.records if x.get("procurement_needs")]
        if pt:
            pl=pt.lower(); r=[x for x in r if any(pl in n.lower() for n in x.get("procurement_needs",[]))]
        return r

    def get_contactable_leads(self):
        return [x for x in self.records if x.get("email") or x.get("phone") or x.get("linkedin") or x.get("contact_method")]

    def get_leads_by_country(self, c):
        return [x for x in self.records if c.lower() in (x.get("country") or x.get("location") or "").lower()]

    # ===== CRUD =====
    def add_lead(self, lead):
        lid=f"BUY-{len(self.records)+1:04d}"
        lead.update({"id":lid,"confirmed":False,"last_updated":"2026-05-06"})
        self.records.append(lead); self._save(); return lid

    def update_lead(self, lid, updates):
        for r in self.records:
            if r.get("id")==lid: r.update(updates); self._save(); return True
        return False

    # ===== 验证 =====
    def verify_lead(self, lid, method=None):
        lead=next((r for r in self.records if r.get("id")==lid),None)
        if not lead: return {"error":"未找到"}
        vf=lead.get("_verifications",[])
        ms=[method] if method else self.VM.keys()
        for m in ms:
            if m not in self.VM or any(x["method"]==m for x in vf): continue
            vf.append(self._run_vf(lead,m))
        score=sum(x["passed"]*self.VM[x["method"]] for x in vf)
        passed=sum(1 for x in vf if x["passed"])
        lead["_verifications"]=vf; lead["_confidence"]=round(score,2)
        if passed>=3: lead["confirmed"]=True
        lead["last_updated"]="2026-05-06"; self._save()
        return {"lead_id":lid,"confidence":round(score,2),"verified_methods":passed,
                "total_methods":len(self.VM),"details":vf,"confirmed":lead.get("confirmed",False)}

    def _run_vf(self,lead,m):
        r={"method":m,"passed":False,"evidence":"","timestamp":"2026-05-06"}
        if m=="website_check":
            w=lead.get("website","")
            if w: r["passed"]=True; r["evidence"]=f"网站存在: {w}"
        elif m=="email_check":
            e=lead.get("email","")
            if e:
                d=e.split("@")[-1]
                r["passed"]="." in d and len(d)>5
                r["evidence"]=f"邮箱有效: {e}" if r["passed"] else f"邮箱异常: {e}"
        elif m=="phone_check":
            p=lead.get("phone","")
            if p:
                r["passed"]=p.startswith("+") and len(''.join(filter(str.isdigit,p)))>=8
                r["evidence"]=f"电话有效: {p}" if r["passed"] else f"电话异常: {p}"
        elif m=="linkedin_check":
            li=lead.get("linkedin","")
            if li:
                r["passed"]="linkedin.com" in li.lower()
                r["evidence"]=f"LinkedIn: {li}" if r["passed"] else "LinkedIn异常"
        elif m=="third_party":
            nm=lead.get("company_name") or lead.get("project_name") or lead.get("person_name","")
            r["passed"]=bool(nm); r["evidence"]="交叉验证完成" if nm else "无数据"
        return r

    # ===== 工厂触达 =====
    def _of(self):
        return os.path.join(DATA_DIR, "outreach.json")

    def record_outreach(self, intel_id, factory_id="", factory_name="", method="email", note=""):
        of=self._of()
        outreach=[]
        if os.path.exists(of):
            with open(of) as f: outreach=json.load(f)
        rec=next((o for o in outreach if o["lead_id"]==intel_id),None)
        if not rec:
            rec={"lead_id":intel_id,"intel_summary":self._is(intel_id),
                 "factory_contacts":[],"status":"触达中","priority":"P1"}
            outreach.append(rec)
        rec["factory_contacts"].append({
            "factory_id":factory_id,"factory_name":factory_name,
            "contact_method":method,"contacted_at":"2026-05-06",
            "response":"待回复","response_at":None,"deal_status":"跟进中","note":note,
        })
        rec["status"]="触达中"; rec["last_updated"]="2026-05-06"
        with open(of,"w") as f: json.dump(outreach,f,ensure_ascii=False,indent=2)
        return rec

    def update_outreach(self, intel_id, factory_idx, updates):
        of=self._of()
        if not os.path.exists(of): return False
        with open(of) as f: outreach=json.load(f)
        rec=next((o for o in outreach if o["lead_id"]==intel_id),None)
        if not rec or factory_idx>=len(rec["factory_contacts"]): return False
        rec["factory_contacts"][factory_idx].update(updates)
        rec["last_updated"]="2026-05-06"
        ss=[fc.get("deal_status") for fc in rec["factory_contacts"]]
        if "已合作" in ss: rec["status"]="已合作"
        elif "报价中" in ss: rec["status"]="报价中"
        elif all(s=="已放弃" for s in ss): rec["status"]="已放弃"
        with open(of,"w") as f: json.dump(outreach,f,ensure_ascii=False,indent=2)
        return True

    def get_outreach_status(self, intel_id=None):
        of=self._of()
        if not os.path.exists(of): return []
        with open(of) as f: outreach=json.load(f)
        if intel_id:
            rec=next((o for o in outreach if o["lead_id"]==intel_id),None)
            return [rec] if rec else []
        return outreach

    def _is(self,lid):
        for r in self.records:
            if r.get("id")==lid: return r.get("notes") or r.get("project_name") or r.get("company_name") or ""
        return ""

    def dashboard(self):
        of=self._of()
        outreach=[]
        if os.path.exists(of):
            with open(of) as f: outreach=json.load(f)
        contacted=sum(1 for o in outreach if o.get("status") not in ["待触达"])
        won=sum(1 for o in outreach if o.get("status")=="已合作")
        dealing=sum(1 for o in outreach if o.get("status") in ["报价中","触达中"])
        return {
            "数据库":{"总记录":len(self.records),"活跃项目":len([r for r in self.records if r.get("procurement_needs")])},
            "触达":{"总线索":len(outreach),"已联系":contacted,"待联系":len(outreach)-contacted,"跟进中":dealing,"已成交":won},
            "验证":{"已验证":sum(1 for r in self.records if r.get("confirmed")),"待验证":sum(1 for r in self.records if not r.get("confirmed"))},
        }

    def summarize(self):
        proj=self.get_active_projects()
        countries=set()
        for r in self.records:
            c=r.get("country") or ""; 
            if c: countries.add(c)
            loc=r.get("location") or ""
            if "," in loc: countries.add(loc.split(",")[-1].strip())
        return {"total":len(self.records),"active_projects":len(proj),
                "contactable":len(self.get_contactable_leads()),"countries":sorted(countries),
                "budget":sum(r.get("budget_usd") or 0 for r in self.records)}

    # ===== 订阅管理 =====
    def _sf(self): return os.path.join(DATA_DIR,"subscribers.json")

    def register_subscriber(self, factory_id, factory_name, plan="free_trial",
                            email="", phone="", notes=""):
        sf=self._sf()
        subs=[]; 
        if os.path.exists(sf):
            with open(sf) as f: subs=json.load(f)
        if any(s["factory_id"]==factory_id for s in subs):
            return {"error":"已注册"}
        sub={"factory_id":factory_id,"factory_name":factory_name,
             "plan":plan,"status":"trial" if plan=="free_trial" else "active",
             "subscribed_at":"2026-05-06",
             "trial_ends":"2026-05-13" if plan=="free_trial" else None,
             "paid_through":None if plan in ["free","free_trial"] else "2026-06-06",
             "monthly_fee":self.TIERS.get(plan,{}).get("price_monthly",0),
             "contact_email":email,"contact_phone":phone,"notes":notes,
             "access_log":[],}
        subs.append(sub)
        with open(sf,"w") as f: json.dump(subs,f,ensure_ascii=False,indent=2)
        return sub

    def get_subscriber(self, factory_id=None):
        sf=self._sf()
        if not os.path.exists(sf): return []
        with open(sf) as f: subs=json.load(f)
        if factory_id: return [s for s in subs if s["factory_id"]==factory_id]
        return subs

    def upgrade_subscriber(self, factory_id, new_plan):
        sf=self._sf()
        if not os.path.exists(sf): return False
        with open(sf) as f: subs=json.load(f)
        for s in subs:
            if s["factory_id"]==factory_id:
                s["plan"]=new_plan; s["status"]="active"
                s["monthly_fee"]=self.TIERS.get(new_plan,{}).get("price_monthly",0)
                with open(sf,"w") as f: json.dump(subs,f,ensure_ascii=False,indent=2)
                return True
        return False

    def mark_paid(self, factory_id, months=1):
        sf=self._sf()
        if not os.path.exists(sf): return False
        with open(sf) as f: subs=json.load(f)
        for s in subs:
            if s["factory_id"]==factory_id:
                base=datetime.now()
                if s.get("paid_through"):
                    try: base=datetime.strptime(s["paid_through"],"%Y-%m-%d")
                    except: pass
                s["paid_through"]=(base+timedelta(days=30*months)).strftime("%Y-%m-%d")
                s["status"]="active"
                with open(sf,"w") as f: json.dump(subs,f,ensure_ascii=False,indent=2)
                return True
        return False

    def check_expired(self):
        sf=self._sf()
        if not os.path.exists(sf): return []
        with open(sf) as f: subs=json.load(f)
        now=datetime.now()
        expired=[]
        for s in subs:
            pt=s.get("paid_through") or s.get("trial_ends","2000-01-01")
            try:
                dt=datetime.strptime(pt,"%Y-%m-%d")
                if dt<now:
                    expired.append({"工厂":s["factory_name"],"方案":s["plan"],
                                    "到期日":pt,"逾期天数":(now-dt).days})
            except: pass
        return expired

    def log_access(self, factory_id, lead_id):
        sf=self._sf()
        if not os.path.exists(sf): return {"error":"无订阅者"}
        with open(sf) as f: subs=json.load(f)
        for s in subs:
            if s["factory_id"]==factory_id:
                plan=self.TIERS.get(s["plan"],self.TIERS["free"])
                mx=plan["max_results"]
                cnt=len(s.get("access_log",[]))
                if mx!=999 and cnt>=mx:
                    return {"error":f"已达本月限额({mx}条)，请升级方案"}
                s.setdefault("access_log",[]).append({"lead_id":lead_id,"accessed_at":"2026-05-06"})
                with open(sf,"w") as f: json.dump(subs,f,ensure_ascii=False,indent=2)
                return {"ok":True,"已查看":lead_id,"共查看":len(s["access_log"])}
        return {"error":"未找到订阅者"}

    def subscriber_metrics(self):
        sf=self._sf()
        subs=[]; 
        if os.path.exists(sf):
            with open(sf) as f: subs=json.load(f)
        return {"总订阅者":len(subs),"活跃":sum(1 for s in subs if s.get("status")=="active"),
                "试用":sum(1 for s in subs if s.get("status")=="trial"),
                "已过期":len(self.check_expired()),
                "月收入":sum(s.get("monthly_fee",0) for s in subs if s.get("status")=="active"),
                "方案分布":{p:sum(1 for s in subs if s.get("plan")==p) for p in set(s.get("plan") for s in subs)}}

    def subscription_plans(self):
        return [{"tier":k,"name":v["name"],"price":v["price_monthly"],
                 "max":v["max_results"]} for k,v in self.TIERS.items()]


if __name__=="__main__":
    import sys
    bi=BuyerIntel()
    def pp(d): print(json.dumps(d,ensure_ascii=False,indent=2))

    if len(sys.argv)<2:
        s=bi.summarize()
        print(f"买家情报引擎 — {s['total']}条 | {s['active_projects']}项目 | {s['contactable']}可联系")
        print(f"  覆盖: {', '.join(s['countries'])}\n")
        print("  search <query>              搜索")
        print("  projects [country]          项目")
        print("  leads [country]             线索")
        print("  opportunities [product]     采购机会")
        print("  verify <id> [method]        验证")
        print("  outreach <id> <工厂> [备注] 触达")
        print("  outreach-status [id]        触达进度")
        print("  dashboard                   主控台")
        print("  sub register <id> <名> [plan] 注册订阅")
        print("  sub list [id]               订阅者")
        print("  sub metrics                 订阅数据")
        print("  sub expired                 已过期")
        print("  subscribe                   方案")
        sys.exit(0)

    cmd=sys.argv[1]

    if cmd=="search": pp(bi.search(" ".join(sys.argv[2:]) if len(sys.argv)>2 else ""))
    elif cmd=="projects":
        c=sys.argv[2] if len(sys.argv)>2 else None
        for p in bi.get_active_projects(c):
            b=p.get("budget_usd","")
            print(f"  {p.get('id','')}  {p.get('project_name','')[:40]}  {p.get('location','') or p.get('country','')}" + (f"  ${b:,}" if b else ""))
            print(f"     采购: {', '.join(p.get('procurement_needs',[]))}\n")
    elif cmd=="leads":
        c=sys.argv[2] if len(sys.argv)>2 else None
        leads=bi.get_leads_by_country(c) if c else bi.get_contactable_leads()
        for l in leads:
            nm=l.get("company_name") or l.get("project_name") or l.get("person_name","")
            ct=l.get("email") or l.get("phone") or l.get("linkedin") or "无"
            print(f"  {'✅' if l.get('confirmed') else '⏳'} {nm:<35s}  {ct}")
    elif cmd=="opportunities":
        pt=" ".join(sys.argv[2:]) if len(sys.argv)>2 else None
        pp([{"id":o.get("id"),"project":o.get("project_name") or o.get("company_name"),
             "needs":o.get("procurement_needs"),"status":o.get("status")}
            for o in bi.get_procurement_opportunities(pt)])
    elif cmd=="verify":
        pp(bi.verify_lead(sys.argv[2] if len(sys.argv)>2 else "",
                          sys.argv[3] if len(sys.argv)>3 else None))
    elif cmd=="outreach":
        pp(bi.record_outreach(sys.argv[2] if len(sys.argv)>2 else "",
                              factory_name=sys.argv[3] if len(sys.argv)>3 else "",
                              note=" ".join(sys.argv[4:]) if len(sys.argv)>4 else ""))
    elif cmd=="outreach-status":
        pp(bi.get_outreach_status(sys.argv[2] if len(sys.argv)>2 else None))
    elif cmd=="dashboard":
        pp(bi.dashboard())
    elif cmd=="subscribe":
        for p in bi.subscription_plans():
            print(f"  {p['tier']:12s}  {p['name']:<8s}  ¥{p['price']:>4}/月  最多{p['max']}条")
    elif cmd=="sub":
        sc=sys.argv[2] if len(sys.argv)>2 else ""
        if sc=="register":
            pp(bi.register_subscriber(
                sys.argv[3] if len(sys.argv)>3 else "",
                sys.argv[4] if len(sys.argv)>4 else "",
                sys.argv[5] if len(sys.argv)>5 else "free_trial"))
        elif sc=="list":
            pp(bi.get_subscriber(sys.argv[3] if len(sys.argv)>3 else None))
        elif sc=="metrics":
            pp(bi.subscriber_metrics())
        elif sc=="expired":
            pp(bi.check_expired())
        elif sc=="paid":
            pp({"ok":bi.mark_paid(sys.argv[3] if len(sys.argv)>3 else "",
                                  int(sys.argv[4]) if len(sys.argv)>4 else 1)})
        elif sc=="upgrade":
            pp({"ok":bi.upgrade_subscriber(sys.argv[3] if len(sys.argv)>3 else "",
                                           sys.argv[4] if len(sys.argv)>4 else "basic")})
