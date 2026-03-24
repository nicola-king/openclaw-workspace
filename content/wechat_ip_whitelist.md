# 微信公众号 IP 白名单配置

## 当前服务器 IP

- **IPv4**: `106.92.49.165`
- **IPv6**: `::ffff:106.92.49.165`

## 配置步骤

1. 登录 https://mp.weixin.qq.com
2. 左侧菜单：**开发** → **基本配置**
3. 找到 **IP 白名单** 设置
4. 点击 **修改**
5. 添加 IP：`106.92.49.165`
6. 保存（可能需要管理员扫码）

## 验证

添加后等待 1-2 分钟，然后执行：

```bash
export WECHAT_APPID=wx720a4c489fec9df3
export WECHAT_APP_SECRET=94066275ad79af78b29b3c5f1ef7660c
cd ~/.openclaw/workspace
md2wechat --markdown content/wechat_first_post.md --title "太一 0 成本启动" --author "太一" --summary "这是一个关于 AGI、套利和零成本启动的故事"
```

## 备用方案（纯文字版）

如果暂时无法添加白名单，可以先发布纯文字版：

```bash
md2wechat --markdown content/wechat_first_post.md --title "太一 0 成本启动" --author "太一" --summary "这是一个关于 AGI、套利和零成本启动的故事"
```

（需要移除文章中的图片）

---

*创建时间：2026-03-24 15:30 | 太一*
