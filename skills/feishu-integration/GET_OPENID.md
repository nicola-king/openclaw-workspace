# 获取用户 Open ID 指南

> **应用**: 太一 AI (cli_a9086d6b5779dcc1)
> **时间**: 2026-05-04
> **状态**: 需要获取用户 open_id

---

## 🔍 获取 Open ID 的方法

### 方法1: 通过飞书开放平台查询

1. 访问 https://open.feishu.cn/app/cli_a9086d6b5779dcc1/
2. 点击左侧菜单 **"用户管理"**
3. 找到你的用户，查看 open_id

### 方法2: 通过 API 查询

```python
import lark_oapi
from lark_oapi.api.contact.v3 import *
from lark_oapi.core.model.request_option import RequestOption

# 创建客户端
client = lark_oapi.Client.builder() \
    .app_id("cli_a9086d6b5779dcc1") \
    .app_secret("tXHOop03ZHQynCRuEPkambASNori3KhZ") \
    .build()

# 获取 Token
from lark_oapi.api.auth.v3 import *
req = InternalTenantAccessTokenRequest.builder() \
    .request_body(InternalTenantAccessTokenRequestBody.builder()
        .app_id("cli_a9086d6b5779dcc1")
        .app_secret("tXHOop03ZHQynCRuEPkambASNori3KhZ")
        .build()) \
    .build()

resp = client.auth.v3.tenant_access_token.internal(req)
import json
raw_content = json.loads(resp.raw.content)
token = raw_content.get('tenant_access_token', '')

# 查询用户列表
req = FindByDepartmentUserRequest.builder() \
    .department_id_type('open_department_id') \
    .department_id('0') \
    .page_size(10) \
    .build()

option = RequestOption.builder() \
    .tenant_access_token(token) \
    .build()

resp = client.contact.v3.user.find_by_department(req, option)

if resp.success():
    data = json.loads(resp.raw.content)
    users = data.get('data', {}).get('items', [])
    for user in users:
        print(f"姓名: {user.get('name', '')}")
        print(f"Open ID: {user.get('open_id', '')}")
        print(f"User ID: {user.get('user_id', '')}")
        print("---")
```

### 方法3: 通过 Webhook 事件获取

当用户发送消息给 Bot 时，Webhook 事件会包含用户的 open_id：

```json
{
  "event": {
    "sender": {
      "sender_id": {
        "open_id": "ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "union_id": "on_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "user_id": "xxxxxxxx"
      }
    }
  }
}
```

---

## 📝 配置到系统

获取 open_id 后，更新配置文件：

```yaml
# skills/feishu-integration/config.yaml

# 管理员配置
admin_open_id: "ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 默认推送目标
default_chat_id: "oc_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

---

## 🚀 测试发送消息

配置完成后，运行测试：

```bash
cd /home/sayelf/.openclaw/workspace/skills/feishu-integration
source /home/sayelf/.openclaw/workspace/venv-feishu/bin/activate
python3 test_message.py
```

---

## 🔗 相关链接

- [飞书用户 ID 说明](https://open.feishu.cn/document/server-docs/getting-started/user-id-types)
- [获取用户列表 API](https://open.feishu.cn/document/server-docs/contact-v3/user/find_by_department)

---

*太一 AGI · 获取 Open ID 指南*
