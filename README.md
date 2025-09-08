# Automated Ameritrade Trading Bot

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](#) \[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)]

A **Python**-powered trading system that leverages the TD Ameritrade API to automate data collection, indicator computation, portfolio management, and order execution. Designed for both paper and live trading, this bot framework helps you prototype strategies, monitor risk, and execute trades seamlessly.

---

## 🚀 Features

* **Seamless TD Ameritrade Integration**: OAuth session management, real-time quotes, and historical bars.
* **Extensible Indicators**: Built‑in RSI, SMA, EMA, Bollinger Bands, MACD, ATR, and more—plus custom signal thresholds.
* **Portfolio Engine**: Track positions, P/L, risk metrics, and allocation by asset type.
* **Order Abstraction**: Create market, limit, stop, stop‑limit, trailing stops, and child orders in a unified API.
* **Paper & Live Modes**: Toggle paper trading for safe testing; switch to live execution with one flag.
* **Continuous Loop**: Fetch latest bars, refresh indicators, check signals, and execute orders on a schedule.
* **JSON Logging**: Persist executed orders and market snapshots for audit or backtesting.

---

## 📐 Architecture

```
configs/                # config.ini template (CLIENT_ID, REDIRECT_URI, etc.)
pyrobot/                # core library
├─ indicators.py        # compute and manage technical indicators
├─ portfolio.py         # positions, allocations, and risk metrics
├─ stock_frame.py       # pandas wrapper for symbol-indexed time series
├─ trades.py            # build and manage TD order payloads
├─ trading_robot_indicators.py # example indicator strategy
└─ robot.py             # PyRobot: session, data I/O, and execution engine

run_robot.py            # example script: assemble components and run the loop
data/                   # output JSON logs (orders, snapshots)
write_config.py         # helper to generate config/config.ini
```

---

## ⚙️ Prerequisites

* Python **3.8** or higher
* TD Ameritrade Developer account + API key
* Install dependencies:

  ```bash
  pip install td-ameritrade-python-api pandas numpy
  ```

---

## 🔧 Installation & Setup

1. **Fork & Clone**

   ```bash
   git clone https://github.com/<your-username>/ameritrade-bot.git
   cd ameritrade-bot
   ```
2. **Create & Activate** a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\\Scripts\\activate  # Windows
   ```
3. **Install** required packages:

   ```bash
   pip install -r requirements.txt
   ```
4. **Generate** configuration file:

   ```bash
   python write_config.py
   ```
5. **Edit** `configs/config.ini` with your:

   * `CLIENT_ID` (consumer key)
   * `REDIRECT_URI`
   * `JSON_PATH` (token storage)
   * `ACCOUNT_NUMBER`

---

## 🎯 Usage

### Paper Trading (Safe Testing)

```bash
python run_robot.py --paper
```

### Live Trading

```bash
python run_robot.py
```

### Custom Strategy

* Modify `run_robot.py` or build new orchestrator scripts:

  1. Instantiate `PyRobot`
  2. Create `Portfolio` and add positions
  3. Fetch and wrap data in `StockFrame`
  4. Add indicators via `Indicators`
  5. Set signal thresholds
  6. Loop over `get_latest_bar()`, `refresh()`, `check_signals()`, `execute_signals()`

---

## 🔧 Configuration Options

```ini
[main]
CLIENT_ID     = YOUR_CONSUMER_KEY
REDIRECT_URI  = https://yourapp/callback
JSON_PATH     = /path/to/credentials.json
ACCOUNT_NUMBER= 123456789
```

Use `write_config.py` to scaffold this file automatically.

---

## 📈 Roadmap

* **Backtesting Module**: Simulate strategies offline using historical data.
* **Risk Controls**: Position sizing, max drawdown limits, stop‑loss pools.
* **Advanced Indicators**: Ichimoku, VWAP, Heikin‑Ashi candles.
* **Multi‑Broker Support**: Integrate Alpaca, Interactive Brokers, etc.
* **Alerts & Notifications**: Slack, email, SMS alerts on events.
* **Web Dashboard**: Monitor P/L, live charts, order status.
* **Docker & CI/CD**: Containerize for cloud deployment, automated tests.

---

## 🤝 Contributing

1. **Fork** the project.
2. Create a **feature branch**: `git checkout -b feature/awesome`.
3. **Commit** changes with clear messages.
4. **Push** and open a **Pull Request**.
5. Ensure **linting** and **unit tests** pass.

Please follow our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---
