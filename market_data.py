import alpaca_trade_api as tradeapi
from datetime import datetime, timedelta
import config
from logger import logger
import pytz

class MarketData:
    def __init__(self):
        self.api = tradeapi.REST(
            config.ALPACA_API_KEY,
            config.ALPACA_SECRET_KEY,
            config.ALPACA_BASE_URL
        )

    def is_market_open(self):
        """Check if market is currently open"""
        try:
            clock = self.api.get_clock()
            return clock.is_open
        except Exception as e:
            logger.error(f"Failed to check market status: {e}")
            return False

    def get_account(self):
        """Get account information"""
        try:
            account = self.api.get_account()
            logger.info(f"Account: Cash=${account.cash}, Portfolio=${account.portfolio_value}")
            return account
        except Exception as e:
            logger.error(f"Failed to get account: {e}")
            raise

    def get_positions(self):
        """Get current positions"""
        try:
            positions = self.api.list_positions()
            logger.info(f"Current positions: {len(positions)}")
            return positions
        except Exception as e:
            logger.error(f"Failed to get positions: {e}")
            raise

    def get_current_price(self, symbol):
        """Get current price for a symbol"""
        try:
            barset = self.api.get_latest_trade(symbol)
            price = barset.price
            logger.info(f"{symbol} current price: ${price}")
            return price
        except Exception as e:
            logger.error(f"Failed to get price for {symbol}: {e}")
            raise

    def get_historical_data(self, symbol, days=30):
        """Get historical price data"""
        try:
            end = datetime.now()
            start = end - timedelta(days=days)

            barset = self.api.get_bars(
                symbol,
                tradeapi.TimeFrame.Day,
                start=start.strftime('%Y-%m-%d'),
                end=end.strftime('%Y-%m-%d')
            ).df

            logger.info(f"Retrieved {len(barset)} days of data for {symbol}")
            return barset
        except Exception as e:
            logger.error(f"Failed to get historical data for {symbol}: {e}")
            raise
