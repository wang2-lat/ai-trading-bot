import config
from logger import logger
from market_data import MarketData
from analyzer import TechnicalAnalyzer
from risk_manager import RiskManager
from dataclasses import dataclass

# Trading constants
MIN_CONFIDENCE_THRESHOLD = 60

@dataclass
class TradeContext:
    """Context for trade execution"""
    symbol: str
    recommendation: dict
    current_price: float
    position_info: dict
    positions: list
    risk_manager: RiskManager

class Trader:
    def __init__(self):
        self.market_data = MarketData()
        self.analyzer = TechnicalAnalyzer()

    def execute_trading_cycle(self):
        """Execute one complete trading cycle"""
        logger.info("=" * 60)
        logger.info("Starting trading cycle")
        logger.info("=" * 60)

        try:
            # Check if market is open
            if not self.market_data.is_market_open():
                logger.warning("Market is closed. Skipping trading cycle.")
                return

            # Get account and positions
            account = self.market_data.get_account()
            positions = self.market_data.get_positions()
            risk_manager = RiskManager(account)

            # Check stop losses first
            self._check_stop_losses(positions, risk_manager)

            # Analyze and trade each target symbol
            self._analyze_and_trade(positions, risk_manager)

            logger.info("Trading cycle completed successfully")

        except Exception as e:
            logger.error(f"Trading cycle failed: {e}")
            raise

    def _check_stop_losses(self, positions, risk_manager):
        """Check and execute stop losses"""
        logger.info("Checking stop losses...")
        stop_loss_signals = risk_manager.check_stop_loss(positions)

        for signal in stop_loss_signals:
            self._sell_position(signal['symbol'], signal['qty'], "STOP_LOSS")

    def _analyze_and_trade(self, positions, risk_manager):
        """Analyze each symbol and execute trades"""
        logger.info(f"Analyzing {len(config.TARGET_SYMBOLS)} symbols...")

        for symbol in config.TARGET_SYMBOLS:
            try:
                self._process_symbol(symbol, positions, risk_manager)
            except Exception as e:
                logger.error(f"Failed to process {symbol}: {e}")
                continue

    def _process_symbol(self, symbol, positions, risk_manager):
        """Process a single symbol"""
        logger.info(f"\n--- Processing {symbol} ---")

        # Get market data
        current_price = self.market_data.get_current_price(symbol)
        historical_data = self.market_data.get_historical_data(symbol, config.HISTORY_DAYS)

        # Get position info
        position_info = risk_manager.get_position_info(symbol, positions)

        # Prepare account info for AI
        account_info = {
            'cash': risk_manager.cash,
            'position_count': len(positions)
        }

        # Get AI recommendation
        recommendation = self.analyzer.analyze_stock(
            symbol, current_price, historical_data,
            position_info, account_info
        )

        # Execute based on recommendation
        ctx = TradeContext(symbol, recommendation, current_price, position_info, positions, risk_manager)
        self._execute_recommendation(ctx)

    def _execute_recommendation(self, ctx: TradeContext):
        """Execute trading action based on AI recommendation"""
        action = ctx.recommendation['action']
        confidence = ctx.recommendation['confidence']

        if confidence < MIN_CONFIDENCE_THRESHOLD:
            logger.info(f"Skipping {ctx.symbol}: confidence too low ({confidence}%)")
            return

        if action == "BUY":
            self._handle_buy(ctx)
        elif action == "SELL":
            self._handle_sell(ctx)
        else:
            logger.info(f"Holding {ctx.symbol}")

    def _handle_buy(self, ctx: TradeContext):
        """Handle buy action"""
        if ctx.position_info:
            logger.info(f"Already holding {ctx.symbol}, skipping buy")
        elif ctx.risk_manager.can_open_position(len(ctx.positions)):
            qty = ctx.risk_manager.calculate_position_size(ctx.symbol, ctx.current_price)
            if qty > 0:
                self._buy_position(ctx.symbol, qty)
        else:
            logger.info(f"Cannot buy {ctx.symbol}: max positions reached")

    def _handle_sell(self, ctx: TradeContext):
        """Handle sell action"""
        if ctx.position_info:
            self._sell_position(ctx.symbol, ctx.position_info['qty'], "AI_RECOMMENDATION")
        else:
            logger.info(f"No position to sell for {ctx.symbol}")

    def _buy_position(self, symbol, qty):
        """Execute buy order"""
        try:
            logger.info(f"BUYING {qty} shares of {symbol}")
            order = self.market_data.api.submit_order(
                symbol=symbol,
                qty=qty,
                side='buy',
                type='market',
                time_in_force='day'
            )
            logger.info(f"Buy order submitted: {order.id}")
        except Exception as e:
            logger.error(f"Failed to buy {symbol}: {e}")

    def _sell_position(self, symbol, qty, reason):
        """Execute sell order"""
        try:
            logger.info(f"SELLING {qty} shares of {symbol} (Reason: {reason})")
            order = self.market_data.api.submit_order(
                symbol=symbol,
                qty=qty,
                side='sell',
                type='market',
                time_in_force='day'
            )
            logger.info(f"Sell order submitted: {order.id}")
        except Exception as e:
            logger.error(f"Failed to sell {symbol}: {e}")
