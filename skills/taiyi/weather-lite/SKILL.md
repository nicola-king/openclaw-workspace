# weather-lite - 气象数据采集（免费版）

> 自动采集气象数据，每天早上推送到你微信

---

## 功能

- ✅ 自动采集指定城市气象数据
- ✅ 每日 7:00 定时执行
- ✅ 推送到微信/Telegram
- ✅ 数据存到本地数据库

**限制：** 仅限 1 个城市（付费版支持 28 城市）

---

## 安装

```bash
npx clawhub install taiyi-weather-lite
```

---

## 配置

安装后编辑 `~/.taiyi/weather-lite/config.json`：

```json
{
  "city": "Beijing",
  "notify_channel": "wechat",
  "notify_time": "07:00"
}
```

---

## 使用

**自动模式：**
```bash
# 配置后自动运行，每日 7:00 推送
```

**手动模式：**
```bash
taiyi weather-lite --city Beijing
```

---

## 输出示例

```
【气象日报 · 北京】2026-03-24
温度：15°C ~ 25°C
降水概率：30%
湿度：45%
风力：北风 3 级

数据来源：NOAA + WMO
```

---

## 付费升级

需要多城市监控？升级 **weather-pro**：

```bash
npx clawhub install taiyi-weather-pro
```

**付费版功能：**
- 28 城市同时监控
- 气象预警通知
- 历史数据对比
- 数据导出 Excel

**价格：** ¥99/月

---

## 技术支持

- 公众号：SAYELF 山野精灵
- Twitter: @SayelfTea
- GitHub: github.com/nicola-king/zhiji-e

---

*太一 · 2026 年 3 月*
