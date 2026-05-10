{
  "_version": "1.0.0",
  "_description": "智能网络路由配置",

  "proxy": {
    "enabled": true,
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
    "socks": "socks://127.0.0.1:7891",
    "health_check_url": "https://www.google.com",
    "health_check_interval": 300,
    "timeout_seconds": 10
  },

  "domestic": {
    "direct": true,
    "dns_server": "114.114.114.114",
    "fallback_dns": "223.5.5.5"
  },

  "routing_rules": {
    "domains_domestic": [
      "*.baidu.com", "*.qq.com", "*.weixin.qq.com", "*.tencent.com",
      "*.aliyun.com", "*.taobao.com", "*.tmall.com", "*.jd.com",
      "*.163.com", "*.126.com", "*.sina.com.cn", "*.weibo.com",
      "*.douyin.com", "*.toutiao.com", "*.xiaohongshu.com",
      "*.zhihu.com", "*.bilibili.com", "*.csdn.net", "*.cnblogs.com",
      "*.oschina.net", "*.gitee.com", "*.cloudflare.com.cn",
      "*.bytedance.com", "*.meituan.com", "*.dianping.com",
      "*.ctrip.com", "*.qunar.com", "*.fliggy.com",
      "*.gov.cn", "*.edu.cn", "*.org.cn", "*.com.cn", "*.cn",
      "*.didiyun.com", "*.upyun.com", "*.qiniu.com",
      "*.sankuai.com", "*.xiaomi.com", "*.huawei.com",
      "*.zlibrary.cn", "*.pinduoduo.com"
    ],
    "domains_international": [
      "*google*", "*.google.com", "*.googleapis.com", "*.gstatic.com",
      "*github*", "*.github.com", "*.githubusercontent.com",
      "*openai*", "*.openai.com", "*.oaistatic.com", "*.chatgpt.com",
      "*anthropic*", "*.anthropic.com", "*.claude.ai",
      "*meta*", "*.meta.com", "*.facebook.com", "*.instagram.com",
      "*twitter*", "*.twitter.com", "*.x.com",
      "*telegram*", "*.telegram.org", "*.t.me",
      "*discord*", "*.discord.com", "*.discordapp.com",
      "*youtube*", "*.youtube.com", "*.ytimg.com",
      "*reddit*", "*.reddit.com", "*.redditmedia.com",
      "*medium*", "*.medium.com",
      "*docker*", "*.docker.com", "*.docker.io",
      "*npm*", "*.npmjs.com", "*.npmjs.org",
      "*pypi*", "*.pypi.org", "*.python.org",
      "*huggingface*", "*.huggingface.co",
      "*crates.io*", "*rubygems.org*",
      "*stackoverflow*", "*.stackoverflow.com",
      "*amazon*", "*.amazon.com", "*.aws.amazon.com",
      "*microsoft*", "*.microsoft.com", "*.azure.com",
      "*cloudflare*", "*.cloudflare.com"
    ]
  },

  "ai_platforms": {
    "domestic": {
      "deepseek": { "domains": ["*.deepseek.com", "api.deepseek.com"], "route": "direct" },
      "moonshot": { "domains": ["*.moonshot.cn", "api.moonshot.cn"], "route": "direct" },
      "baidu": { "domains": ["*.yiyan.baidu.com", "aip.baidubce.com"], "route": "direct" },
      "aliyun": { "domains": ["dashscope.aliyuncs.com"], "route": "direct" },
      "zhipu": { "domains": ["*.zhipuai.cn", "open.bigmodel.cn"], "route": "direct" },
      "baichuan": { "domains": ["*.baichuan-ai.com"], "route": "direct" },
      "minimax": { "domains": ["*.minimax.com"], "route": "direct" },
      "stepfun": { "domains": ["*.stepfun.com"], "route": "direct" },
      "sensetime": { "domains": ["*.sensetime.com"], "route": "direct" },
      "iflytek": { "domains": ["*.xfyun.cn"], "route": "direct" },
      "kuaishou": { "domains": ["*.kuaishou.com"], "route": "direct" }
    },
    "international": {
      "openai": { "domains": ["*.openai.com", "api.openai.com", "*.chatgpt.com"], "route": "proxy" },
      "anthropic": { "domains": ["*.anthropic.com", "api.anthropic.com"], "route": "proxy" },
      "google": { "domains": ["*.googleapis.com", "generativelanguage.googleapis.com"], "route": "proxy" },
      "meta": { "domains": ["*.meta.ai"], "route": "proxy" },
      "cohere": { "domains": ["*.cohere.com", "api.cohere.com"], "route": "proxy" },
      "mistral": { "domains": ["*.mistral.ai", "api.mistral.ai"], "route": "proxy" },
      "xai": { "domains": ["*.x.ai", "api.x.ai"], "route": "proxy" },
      "perplexity": { "domains": ["*.perplexity.ai", "api.perplexity.ai"], "route": "proxy" },
      "groq": { "domains": ["*.groq.com", "api.groq.com"], "route": "proxy" },
      "together": { "domains": ["*.together.xyz", "api.together.xyz"], "route": "proxy" }
    },
    "hk_nodes": {
      "_warning": "香港AI节点延迟高且不稳定，强制绕过",
      "blocked": [
        "*.hk.*.openai.com", "*.hongkong.*.anthropic.com",
        "api-hk.openai.com", "hk.api.anthropic.com",
        "*.cloud.google.com/hk"
      ],
      "redirect_to": ["us", "jp", "sg", "kr"]
    }
  },

  "domestic_software": {
    "wechat": { "domains": ["*.weixin.qq.com", "*.wx.qq.com"], "route": "direct" },
    "alipay": { "domains": ["*.alipay.com", "*.alipayobjects.com"], "route": "direct" },
    "dingtalk": { "domains": ["*.dingtalk.com"], "route": "direct" },
    "feishu": { "domains": ["*.feishu.cn", "*.feishu.net", "open.feishu.cn"], "route": "direct" },
    "baiduyun": { "domains": ["*.baidupcs.com"], "route": "direct" },
    "netease": { "domains": ["*.music.163.com"], "route": "direct" }
  },

  "intelligent_switching": {
    "enabled": true,
    "health_check_interval": 300,
    "time_based_intervals": {
      "enabled": true,
      "daytime": {
        "start_hour": 8,
        "end_hour": 23,
        "description": "08:00~23:59 每5分钟",
        "interval_seconds": 300
      },
      "nighttime": {
        "start_hour": 0,
        "end_hour": 7,
        "description": "00:00~07:59 每2小时",
        "interval_seconds": 7200
      }
    },
    "retry_count": 3,
    "fallback_timeout": 5,
    "auto_detect": true,
    "custom_dns_enabled": true,
    "geo_detection": {
      "enabled": true,
      "api": "https://ip-api.com/json/",
      "timeout": 3
    },
    "performance_monitoring": {
      "enabled": true,
      "window_minutes": 60,
      "latency_threshold_ms": 2000,
      "packet_loss_threshold": 0.1
    }
  },

  "task_to_route_mapping": {
    "domestic_task": ["local_business", "domestic_api", "feishu_sync", "wechat_monitor"],
    "international_task": ["osint", "github_sync", "global_search", "ai_api_calls"],
    "ai_task": ["llm_inference", "ai_search", "model_download"],
    "blocked_hk_ai": ["openai_api", "anthropic_api", "google_ai_api"]
  }
}
