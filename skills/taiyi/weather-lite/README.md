# weather-lite - 气象数据采集（免费版）

> 自动采集气象数据，每天早上推送到你微信

---

## 快速开始

### 1. 安装

```bash
npx clawhub install taiyi-weather-lite
```

### 2. 配置

编辑 `~/.taiyi/weather-lite/config.json`：

```json
{
  "city": "Beijing",
  "notify_channel": "telegram",
  "notify_time": "07:00"
}
```

### 3. 运行

**手动运行：**
```bash
python3 ~/.taiyi/weather-lite/weather_collector.py --city Beijing
```

**自动运行：**
```bash
# 已配置 cron，每日 07:00 自动执行
```

---

## 功能

- ✅ 自动采集指定城市气象数据
- ✅ 每日 07:00 定时执行
- ✅ 数据存到本地数据库
- ✅ 生成简易报告

**限制：** 仅限 1 个城市

---

## 输出示例

```
【气象日报 · 北京】2026-03-24

当前天气：
温度：15°C
湿度：45%
降水：0mm

今日预报：
最高温：25°C
最低温：12°C
降水总量：0mm

数据来源：Open-Meteo（免费 API）
```

---

## 付费升级

需要多城市监控？升级 **weather-pro**：

- 28 城市同时监控
- 气象预警通知
- 历史数据对比
- 数据导出 Excel

**价格：** ¥99/月

**获取方式：**
```bash
npx clawhub install taiyi-weather-pro
```

---

## 技术支持

- 公众号：SAYELF 山野精灵
- Twitter: @SayelfTea
- GitHub: github.com/nicola-king/zhiji-e

---

*太一 · 2026 年 3 月*
