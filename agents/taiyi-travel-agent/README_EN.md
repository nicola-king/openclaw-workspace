# 🌍 Taiyi Travel Pathfinder Agent

> **Version**: 1.0.0  
> **Created**: 2026-04-14  
> **Author**: Taiyi AGI  
> **License**: MIT

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Status: Production Ready](https://img.shields.io/badge/status-production%20ready-green.svg)]()

---

## 🎯 Overview

Taiyi Travel Pathfinder Agent is an **all-in-one intelligent travel service platform** with 18+ core features, providing end-to-end intelligent travel solutions from planning to ground services.

**Key Features**:
- ✅ Intelligent Travel Planning
- ✅ Multi-City Route Optimization
- ✅ Ground Services (Charter/Airport Pickup/Guide)
- ✅ Provider Onboarding CLI
- ✅ Information Distillation & Fusion
- ✅ Self-Evolving Capability
- ✅ Automatic Knowledge Learning
- ✅ Multi-Platform Push (Telegram/WeChat)

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/nicola-king/taiyi-travel-agent.git
cd taiyi-travel-agent

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from taiyi_travel_agent import TaiyiTravelAgent

# Create Agent
agent = TaiyiTravelAgent()

# Intelligent Travel Planning
plan = agent.plan_trip(
    origin="Beijing",
    destination="Tokyo",
    start_date="2026-05-01",
    end_date="2026-05-07",
    budget=15000,
    travelers=2,
    need_car_rental=True,
    need_local_guide=True
)

# Send to Telegram
agent.send_to_telegram(plan, chat_id="your_chat_id")

# Send to WeChat
agent.send_to_wechat(plan)
```

### Provider Onboarding

```bash
# Hotel onboarding
python3 provider_cli.py hotel register \
  --name "Tokyo Grand Hotel" \
  --location "Tokyo" \
  --price 800 \
  --rating 4.5

# Guide onboarding
python3 provider_cli.py guide register \
  --name "Guide Wang" \
  --location "Tokyo" \
  --language "Chinese/English" \
  --price_per_day 800

# Charter onboarding
python3 provider_cli.py charter register \
  --name "Shenzhou Charter" \
  --location "Tokyo" \
  --car_types Comfort Luxury \
  --price_per_day 600
```

---

## 📋 Core Features

### 1. Intelligent Travel Planning

- Automatic travel mode detection (Domestic/International)
- Smart budget allocation
- Multi-city route optimization
- Travel checklist generation

### 2. Ground Services

- **Charter & Airport Pickup**: Merged charter + airport pickup service
- **Local Guide Service**: Merged companion + guide service
- **All-Inclusive Packages**: One-stop solution

### 3. Provider Onboarding CLI

- Hotel onboarding
- Restaurant onboarding
- Car rental onboarding
- Local guide onboarding
- Charter service onboarding

### 4. Information Distillation & Fusion

- Penetrating domestic internet information (Mafengwo/Qyer/Ctrip/Xiaohongshu/Zhihu)
- Penetrating international internet information (TripAdvisor/Lonely Planet/Booking/Airbnb)
- Information distillation & refinement
- Comparative analysis (Price/Rating/Service)
- Fusion & combination selection
- Intelligent recommendation

### 5. Self-Evolving Capability

- Automatic travel data learning
- Self-optimizing recommendation algorithms
- Capability emergence detection
- Automatic skill creation
- Experience accumulation & sharing

### 6. Automatic Knowledge Learning

- Learning from travel bloggers (10+ bloggers)
- Learning from travel websites (12+ websites)
- Destination guide extraction
- Recommendation algorithm updates

### 7. Multi-Platform Push

- Telegram push
- WeChat push
- Markdown report generation

---

## 📊 Test Results

### Intelligent Travel Planning

```python
plan = agent.plan_trip(
    origin="Beijing",
    destination="Tokyo",
    start_date="2026-05-01",
    end_date="2026-05-07",
    budget=15000,
    travelers=2
)
```

**Output**:
```
✅ Travel Mode: International
✅ Flight Info: 3 options
✅ Budget Allocation: Flight/Accommodation/Meals/Activities/Shopping
✅ Weather: Tokyo weather
✅ Exchange Rates: CNY/USD/EUR/JPY
✅ Travel Checklist: 4 categories, 20+ items
```

### Provider Onboarding

```bash
python3 provider_cli.py hotel register \
  --name "Tokyo Grand Hotel" \
  --location "Tokyo" \
  --price 800 \
  --rating 4.5
```

**Output**:
```
✅ Registration Successful
ID: hotel_20260414171500
Name: Tokyo Grand Hotel
Location: Tokyo
Status: pending (awaiting approval)
```

### Information Distillation & Fusion

```python
distillation = TravelInfoDistillation()
final_plan = distillation.fuse_and_recommend("Tokyo", provider_data)
```

**Output**:
```
✅ Fusion Recommendation Complete
  Information Sources: 9
  Confidence: 90.79%
  Best Choices: 3
```

---

## 📁 Project Structure

```
taiyi-travel-agent/
├── taiyi_travel_agent.py          # Main Agent
├── ground_services.py              # Ground Services Module
├── destination_notices.py          # Destination Notices Module
├── dual_mode_strategy.py           # Dual Mode Strategy Module
├── travel_knowledge_learner.py     # Knowledge Learning Module
├── travel_info_distillation.py     # Information Distillation Module
├── provider_cli.py                 # Provider Onboarding CLI
├── self_evolving_travel_agent.py   # Self-Evolving Module
├── data/
│   ├── providers/                  # Provider Data
│   ├── distillation/               # Distillation Data
│   ├── auto-learning/              # Learning Data
│   └── knowledge/                  # Knowledge Base
├── reports/                        # Reports Directory
└── README.md                       # This file
```

---

## 💰 Business Value

**Provider Value**:
- ✅ Direct platform onboarding
- ✅ Increased exposure opportunities
- ✅ Reduced customer acquisition costs
- ✅ Digital management

**User Value**:
- ✅ One-stop selection
- ✅ Transparent pricing
- ✅ Authentic reviews
- ✅ Intelligent recommendations
- ✅ Save 30%+ travel costs

**Platform Value**:
- ✅ Provider commissions (10-15%)
- ✅ Data accumulation
- ✅ User stickiness
- ✅ Ecosystem closed loop

---

## 🌐 Supported Destinations

### Domestic (China)
- Beijing (History & Culture)
- Shanghai (Modern City)
- Chengdu (Leisure & Food)
- Xi'an (History & Culture)
- Yunnan (Natural Scenery)

### International
- Japan (Culture & Shopping)
- South Korea (Shopping & Food)
- Thailand (Island Vacation)
- Singapore (City Tour)
- France (Culture & Romance)

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Contact

- **Author**: Taiyi AGI
- **GitHub**: https://github.com/nicola-king/taiyi-travel-agent
- **Issues**: https://github.com/nicola-king/taiyi-travel-agent/issues

---

*Taiyi Travel Pathfinder Agent · Taiyi AGI · 2026-04-14*
