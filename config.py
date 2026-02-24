import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
ALPACA_BASE_URL = os.getenv('ALPACA_BASE_URL', 'https://paper-api.alpaca.markets')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
ANTHROPIC_BASE_URL = os.getenv('ANTHROPIC_BASE_URL')

# Trading Configuration
TARGET_SYMBOLS = ['NVDA', 'TSLA', 'META', 'AAPL', 'GOOGL', 'MSFT', 'AMZN']
MAX_POSITIONS = 5
POSITION_SIZE_PCT = 0.20  # 20% per position
STOP_LOSS_PCT = 0.05      # 5% stop loss

# AI Configuration
AI_MODEL = 'claude-3-5-sonnet-20241022'
HISTORY_DAYS = 30
