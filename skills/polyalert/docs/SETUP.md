# PolyAlert Lite Setup Guide

> Step-by-step guide to set up your own Polymarket whale monitoring system

---

## Prerequisites

- Python 3.8+
- Telegram account
- Polymarket account (optional, for API access)

---

## Step 1: Clone Repository

```bash
git clone https://github.com/nicola-king/polymarket-alert.git
cd polymarket-alert
```

---

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 3: Create Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the bot token (format: `XXXXX:XXXXXXXXXXXXXXXXXXXXXXXX`)

---

## Step 4: Configure Bot

Edit `monitor_v1.py` and add your bot token:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

---

## Step 5: Run Monitor

```bash
python monitor_v1.py
```

---

## Step 6: Start Using

1. Open Telegram and search for your bot
2. Send `/start` command
3. You'll receive whale alerts automatically

---

## Troubleshooting

### Bot not responding?
- Check if bot token is correct
- Make sure bot is running (`python monitor_v1.py`)

### No alerts received?
- Check network connection
- Verify Polymarket API is accessible

---

## Upgrade to Pro

Want real-time alerts with no delay?

👉 **[Hunter Pro - $99/month](https://chuanxi.gumroad.com/l/hunter-pro)**

**Pro Features**:
- ✅ Real-time signals (0 delay vs 15 min free)
- ✅ 20+ smart money wallets (vs 5 free)
- ✅ Advanced confidence filter (96%+)
- ✅ Kelly Criterion position sizing
- ✅ Private DM + VIP group access

---

*Setup Guide v1.0 | Questions? Join https://t.me/taiyi_free*
