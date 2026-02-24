# 🤖 AI-Powered Trading Bot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code Quality](https://img.shields.io/badge/Code%20Quality-A%20(97.2%2F100)-brightgreen.svg)](CODE_REVIEW_SKILL_REPORT.md)
[![Tests](https://img.shields.io/badge/Tests-11%2F11%20Passing-success.svg)](test_trading_bot.py)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent algorithmic trading bot that combines technical analysis with risk management to execute automated trades on Alpaca Markets. Built with clean architecture, comprehensive testing, and production-ready code quality.

## ✨ Features

- **📊 Technical Analysis**: RSI, SMA indicators with customizable parameters
- **🛡️ Risk Management**: Position sizing, stop-loss automation, portfolio limits
- **⏰ Market Hours Detection**: Automatic trading suspension when markets are closed
- **📝 Comprehensive Logging**: Detailed execution logs for monitoring and debugging
- **🧪 Fully Tested**: 100% test coverage on core functionality
- **🏗️ Clean Architecture**: SOLID principles, 97.2/100 code quality score

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Alpaca Markets account ([Sign up](https://alpaca.markets))
- Anthropic API key (optional, for future AI features)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/trading-bot.git
cd trading-bot

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your API keys
```

### Configuration

Edit `.env` with your credentials:

```bash
# Alpaca API (Paper Trading)
ALPACA_API_KEY=your_alpaca_key_here
ALPACA_SECRET_KEY=your_alpaca_secret_here
ALPACA_BASE_URL=https://paper-api.alpaca.markets

# Anthropic API (Optional)
ANTHROPIC_API_KEY=your_anthropic_key_here
```

### Run the Bot

```bash
# Run once
python run.py

# Run continuously (every 5 minutes)
./run_bot.sh
```

## 📁 Project Structure

```
trading-bot/
├── analyzer.py          # Technical analysis engine
├── trader.py            # Trading execution logic
├── risk_manager.py      # Risk management system
├── market_data.py       # Market data fetching
├── config.py            # Configuration settings
├── logger.py            # Logging setup
├── run.py               # Main entry point
├── test_trading_bot.py  # Test suite
└── requirements.txt     # Dependencies
```

## 🎯 How It Works

1. **Market Check**: Verifies market is open before trading
2. **Data Collection**: Fetches historical price data for target symbols
3. **Technical Analysis**: Calculates RSI, SMA indicators
4. **Signal Generation**: Identifies buy/sell opportunities
5. **Risk Assessment**: Validates position sizing and portfolio limits
6. **Order Execution**: Submits market orders via Alpaca API
7. **Stop Loss Monitoring**: Automatically exits losing positions

## 📊 Trading Strategy

### Buy Signals
- **Strong Buy**: RSI < 30 + Uptrend (Confidence: 75%)
- **Buy**: Price > SMA(5) > SMA(20) (Confidence: 65%)

### Sell Signals
- **Strong Sell**: RSI > 70 (Confidence: 80%)
- **Sell**: Downtrend detected (Confidence: 70%)

### Risk Management
- **Position Size**: 10% of portfolio per position
- **Stop Loss**: 5% below entry price
- **Max Positions**: 5 concurrent positions
- **Min Confidence**: 60% required for execution

## 🧪 Testing

```bash
# Run all tests
pytest test_trading_bot.py -v

# Run with coverage
pytest test_trading_bot.py --cov=. --cov-report=html
```

**Test Results**: 11/11 passing (100%)

## 📈 Code Quality

This project maintains high code quality standards:

- **Overall Score**: 97.2/100 (Grade A)
- **Code Smells**: 19 (all low severity)
- **SOLID Violations**: 0
- **Test Coverage**: 100% on core modules

See [CODE_REVIEW_SKILL_REPORT.md](CODE_REVIEW_SKILL_REPORT.md) for detailed analysis.

## 🔒 Security

- ✅ API keys stored in `.env` (gitignored)
- ✅ No hardcoded credentials
- ✅ Input validation on all external data
- ✅ Error handling with safe defaults

**Important**: Never commit `.env` file. Always use paper trading for testing.

## 📝 Configuration Options

Edit `config.py` to customize:

```python
TARGET_SYMBOLS = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
HISTORY_DAYS = 30
MAX_POSITIONS = 5
POSITION_SIZE_PCT = 0.10  # 10% per position
STOP_LOSS_PCT = 0.05      # 5% stop loss
```

## 🛠️ Development

### Code Style

This project follows PEP 8 and uses:
- Dataclasses for parameter encapsulation
- Single Responsibility Principle
- Comprehensive error handling
- Descriptive logging

### Adding New Indicators

1. Add calculation method to `TechnicalAnalyzer`
2. Update `_calculate_indicators()` method
3. Modify signal logic in `_check_buy_signals()` / `_check_sell_signals()`
4. Add tests in `test_trading_bot.py`

## 📊 Performance Monitoring

Logs are stored in `logs/trading_bot.log`:

```bash
# View recent activity
tail -f logs/trading_bot.log

# Search for trades
grep "BUYING\|SELLING" logs/trading_bot.log
```

## ⚠️ Disclaimer

**This bot is for educational purposes only.**

- Trading involves substantial risk of loss
- Past performance does not guarantee future results
- Always test with paper trading first
- Never invest more than you can afford to lose
- Consult a financial advisor before live trading

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Alpaca Markets](https://alpaca.markets) for commission-free trading API
- [Anthropic](https://anthropic.com) for Claude AI capabilities
- Code quality validated by Claude Code Reviewer Skill

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/trading-bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/trading-bot/discussions)

---

**⭐ Star this repo if you find it helpful!**

Made with ❤️ by [Your Name]
