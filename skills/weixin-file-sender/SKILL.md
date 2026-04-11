# WeChat File Sender - 微信文件发送器

## 功能
通过微信通道发送文件给用户，支持：
- TXT 文件
- PDF 文件
- MD 文件
- 图片文件
- 视频文件

## 使用方法

### 方式 1: 使用 send_weixin_file 命令
```bash
bash /home/nicola/.openclaw/workspace/skills/weixin-file-sender/send-file.sh <文件路径>
```

### 方式 2: Python 脚本
```python
python3 /home/nicola/.openclaw/workspace/skills/weixin-file-sender/send_file.py <文件路径>
```

## 配置
- 目标用户：当前微信会话用户
- 文件类型：自动检测 MIME 类型
- 文件大小：微信限制 <100MB

## 示例
```bash
# 发送 TXT 报告
bash /home/nicola/.openclaw/workspace/skills/weixin-file-sender/send-file.sh /home/nicola/.openclaw/workspace/reports/taiyi-achievement-report-20260411.txt

# 发送 PDF 报告
bash /home/nicola/.openclaw/workspace/skills/weixin-file-sender/send-file.sh /home/nicola/.openclaw/workspace/reports/taiyi-achievement-report-20260411.pdf
```
