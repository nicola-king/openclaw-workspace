# 📱 飞书集成配置指南

> **创建时间**: 2026-04-11  
> **状态**: 待配置  
> **预计时间**: 10 分钟

---

## 🔐 获取飞书凭证

### 步骤 1: 访问飞书开放平台

访问：https://open.feishu.cn/

### 步骤 2: 登录飞书账号

使用你的飞书企业账号登录

### 步骤 3: 创建企业应用

1. 点击"创建应用"
2. 选择"自建应用"
3. 填写应用名称：`太一 AGI`
4. 填写应用描述：`太一 AGI 飞书集成`
5. 点击"创建"

### 步骤 4: 获取凭证

1. 进入应用管理页面
2. 点击"凭证与基础信息"
3. 复制 **App ID** (格式：`cli_xxxxxxxxxxxxx`)
4. 点击"应用 Secret" → "获取 Secret"
5. 复制 **App Secret** (格式：`xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)

### 步骤 5: 配置权限

1. 点击"权限管理"
2. 搜索并添加以下权限：
   - `im:message` - 消息发送
   - `im:message:read` - 消息读取
   - `docs:doc:readonly` - 文档读取
   - `docs:doc` - 文档编辑
   - `bitable:app:readonly` - 多维表格读取
   - `bitable:app` - 多维表格编辑
   - `contact:user:readonly` - 用户信息读取
3. 点击"申请权限"

### 步骤 6: 发布应用

1. 点击"版本管理与发布"
2. 点击"创建版本"
3. 填写版本号：`1.0.0`
4. 填写版本描述：`初始版本`
5. 点击"发布"

---

## ⚙️ 配置本地文件

### 编辑配置文件

```bash
nano /home/nicola/.openclaw/workspace/config/feishu/config.json
```

### 填写内容

```json
{
  "app_id": "cli_xxxxxxxxxxxxx",
  "app_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "verification_token": "可选",
  "encrypt_key": "可选"
}
```

### 保存退出

按 `Ctrl+O` 保存，按 `Ctrl+X` 退出

---

## ✅ 测试连接

### 运行测试

```bash
python3 /home/nicola/.openclaw/workspace/skills/feishu-integration/feishu_client.py
```

### 成功输出

```
============================================================
📱 飞书客户端测试
============================================================
📱 飞书客户端已初始化
   App ID: cli_xxxxxxxxxxxxx

1. 测试连接...
✅ 访问令牌已获取 (有效期：7200 秒)
✅ 飞书连接测试成功
✅ 连接成功

2. 获取统计...
   配置已加载：True
   令牌已缓存：True

✅ 飞书客户端测试完成!
```

---

## 🚀 使用示例

### 发送消息

```python
from feishu_client import FeishuClient

client = FeishuClient()

# 发送文本消息
client.send_text_message(
    receive_id="ou_xxxxxxxxxxxxx",
    text="Hello from 太一 AGI!"
)

# 发送 Markdown 消息
client.send_markdown_message(
    receive_id="ou_xxxxxxxxxxxxx",
    markdown="# 标题\n\n**内容**"
)
```

### 读取文档

```python
# 读取文档
doc = client.read_document("docxxxxxxxxxxxxxx")
print(doc['title'])
print(doc['content'])
```

### 写入文档

```python
# 写入文档
client.write_document(
    document_id="docxxxxxxxxxxxxxx",
    content="# 新标题\n\n新内容"
)
```

### 多维表格操作

```python
# 获取记录
records = client.get_bitable_records(
    app_id="appxxxxxxxxxxxxxx",
    table_id="tbxxxxxxxxxxxxxx"
)

# 创建记录
client.create_bitable_record(
    app_id="appxxxxxxxxxxxxxx",
    table_id="tbxxxxxxxxxxxxxx",
    fields={"Name": "张三", "Age": 30}
)
```

---

## 🔧 故障排除

### 问题 1: 获取访问令牌失败

**错误**: `invalid param`

**原因**: App ID 或 App Secret 错误

**解决**:
1. 检查配置文件格式
2. 确认 App ID 和 App Secret 正确
3. 确认应用已发布

### 问题 2: 权限不足

**错误**: `no permission`

**原因**: 未申请相应权限

**解决**:
1. 访问飞书开放平台
2. 进入应用权限管理
3. 申请所需权限
4. 等待审批通过

### 问题 3: 用户 ID 不存在

**错误**: `user not found`

**原因**: 用户 ID 错误

**解决**:
1. 在飞书中获取正确的用户 ID
2. 用户 ID 格式：`ou_xxxxxxxxxxxxx`
3. 可通过用户手机号/邮箱查询

---

## 📚 相关文档

- [飞书开放平台](https://open.feishu.cn/)
- [飞书 API 文档](https://open.feishu.cn/document/ukTMukTMukTM/ukTMukTMukTM)
- [消息 API](https://open.feishu.cn/document/ukTMukTMukTM/uETNz4SM1MjLxUzM)
- [文档 API](https://open.feishu.cn/document/ukTMukTMukTM/uQjN1YjL0YDMxUjM)
- [多维表格 API](https://open.feishu.cn/document/ukTMukTMukTM/uQjN1YjL0YDMxUjN)

---

**📱 配置完成后，运行测试验证连接！**

**太一 AGI · 2026-04-11** ✨
