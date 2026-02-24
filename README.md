# AI Trading Bot

A simple but high-quality trading bot that uses Claude AI to analyze markets and make trading decisions on Alpaca Paper Trading.

## Features

- AI-powered market analysis using Claude API
- Aggressive risk profile: 5% stop loss, 20% position size
- Automated trading of tech growth stocks (NVDA, TSLA, META, etc.)
- Risk management with position limits and stop losses
- Comprehensive logging of all operations

## Setup

### 1. Install Dependencies

```bash
cd /Users/wangzhaoye/trading-bot
pip install -r requirements.txt
```

### 2. Configure API Keys

Edit `.env` file and add your API keys:

```bash
# Alpaca Paper Trading API
ALPACA_API_KEY=your_alpaca_api_key
ALPACA_SECRET_KEY=your_alpaca_secret_key
ALPACA_BASE_URL=https://paper-api.alpaca.markets

# Claude API
ANTHROPIC_API_KEY=your_anthropic_api_key
```

Get your API keys:
- Alpaca: https://alpaca.markets (sign up for paper trading)
- Claude: https://console.anthropic.com

### 3. Run the Bot

```bash
python run.py
```

## Configuration

Edit `config.py` to customize:

- `TARGET_SYMBOLS`: Stocks to trade (default: NVDA, TSLA, META, AAPL, GOOGL, MSFT, AMZN)
- `MAX_POSITIONS`: Maximum number of positions (default: 5)
- `POSITION_SIZE_PCT`: Position size as % of portfolio (default: 20%)
- `STOP_LOSS_PCT`: Stop loss percentage (default: 5%)

## How It Works

1. **Check Stop Losses**: Automatically sells positions with >5% loss
2. **AI Analysis**: Claude analyzes each target stock with 30 days of price data
3. **Risk Management**: Enforces position limits and calculates safe position sizes
4. **Execute Trades**: Places market orders based on AI recommendations
5. **Logging**: Records all decisions and trades in `logs/` directory

## Scheduled Execution

To run daily at 10:30 AM ET (after market open):

```bash
crontab -e
```

Add this line:
```
30 10 * * 1-5 cd /Users/wangzhaoye/trading-bot && /usr/bin/python3 run.py
```

## Risk Parameters

- **Stop Loss**: 5% (aggressive)
- **Position Size**: 20% per stock (aggressive)
- **Max Positions**: 5 stocks
- **Confidence Threshold**: 60% (AI must be 60%+ confident)

## Logs

All operations are logged to `logs/trading_YYYYMMDD.log`

## Safety Notes

- This bot uses **paper trading** by default (no real money)
- Always test thoroughly before considering real trading
- Monitor logs regularly
- Adjust risk parameters based on your risk tolerance

## Project Structure

```
trading-bot/
├── config.py           # Configuration and parameters
├── trader.py           # Main trading logic
├── analyzer.py         # AI analysis module
├── market_data.py      # Market data retrieval
├── risk_manager.py     # Risk management
├── logger.py           # Logging utilities
├── run.py              # Entry point
├── requirements.txt    # Dependencies
├── .env                # API keys (not in git)
└── README.md           # This file
```

## Troubleshooting

**API Connection Errors**: Check your API keys in `.env`

**No Trades Executed**: Check logs - AI may recommend HOLD, or confidence may be <60%

**Stop Loss Not Triggering**: Verify positions exist and price data is current

## License

MIT
