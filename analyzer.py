import pandas as pd
import config
from logger import logger
from dataclasses import dataclass

# Technical indicator constants
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
RSI_MAX = 100
RSI_NEUTRAL = 50
MIN_CONFIDENCE = 60

# Signal confidence levels
CONFIDENCE_HIGH = 80
CONFIDENCE_MEDIUM_HIGH = 75
CONFIDENCE_MEDIUM = 65
CONFIDENCE_MEDIUM_LOW = 70
CONFIDENCE_DEFAULT = 50

@dataclass
class AnalysisContext:
    """Context for stock analysis"""
    symbol: str
    current_price: float
    historical_data: pd.DataFrame
    position_info: dict
    account_info: dict

class TechnicalAnalyzer:
    def analyze_stock(self, symbol, current_price, historical_data, position_info, account_info):
        """Analyze stock using technical indicators"""
        ctx = AnalysisContext(symbol, current_price, historical_data, position_info, account_info)

        if ctx.historical_data.empty or len(ctx.historical_data) < 20:
            logger.warning(f"Insufficient data for {ctx.symbol}")
            return {"action": "HOLD", "confidence": 0, "reason": "Insufficient data"}

        try:
            indicators = self._calculate_indicators(ctx.historical_data)
            decision = self._make_decision(ctx, indicators)

            logger.info(f"{ctx.symbol}: {decision['action']} (confidence: {decision['confidence']}%) - {decision['reason']}")
            return decision

        except Exception as e:
            logger.error(f"Technical analysis failed for {ctx.symbol}: {e}")
            return {"action": "HOLD", "confidence": 0, "reason": "Analysis error"}

    def _calculate_indicators(self, historical_data):
        """Calculate technical indicators"""
        return {
            'rsi': self._calculate_rsi(historical_data['close']),
            'sma_short': historical_data['close'].rolling(5).mean().iloc[-1],
            'sma_long': historical_data['close'].rolling(20).mean().iloc[-1]
        }

    def _make_decision(self, ctx, indicators):
        """Make trading decision based on indicators"""
        is_holding = ctx.position_info is not None

        if not is_holding:
            return self._check_buy_signals(ctx, indicators)
        else:
            return self._check_sell_signals(ctx, indicators)

    def _check_buy_signals(self, ctx, indicators):
        """Check for buy signals"""
        rsi = indicators['rsi']
        sma_short = indicators['sma_short']
        sma_long = indicators['sma_long']

        if rsi < RSI_OVERSOLD and ctx.current_price > sma_short > sma_long:
            return {
                "action": "BUY",
                "confidence": CONFIDENCE_MEDIUM_HIGH,
                "reason": f"Oversold (RSI={rsi:.1f}) with uptrend"
            }
        elif ctx.current_price > sma_short > sma_long:
            return {
                "action": "BUY",
                "confidence": CONFIDENCE_MEDIUM,
                "reason": "Strong uptrend"
            }

        return {"action": "HOLD", "confidence": CONFIDENCE_DEFAULT, "reason": "No buy signal"}

    def _check_sell_signals(self, ctx, indicators):
        """Check for sell signals"""
        rsi = indicators['rsi']
        sma_short = indicators['sma_short']
        sma_long = indicators['sma_long']

        if rsi > RSI_OVERBOUGHT:
            return {
                "action": "SELL",
                "confidence": CONFIDENCE_HIGH,
                "reason": f"Overbought (RSI={rsi:.1f})"
            }
        elif ctx.current_price < sma_short < sma_long:
            return {
                "action": "SELL",
                "confidence": CONFIDENCE_MEDIUM_LOW,
                "reason": "Downtrend detected"
            }

        return {"action": "HOLD", "confidence": CONFIDENCE_DEFAULT, "reason": "No sell signal"}

    def _calculate_rsi(self, prices, period=14):
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()

        # Avoid division by zero
        if loss.iloc[-1] == 0:
            return RSI_MAX if gain.iloc[-1] > 0 else RSI_NEUTRAL

        rs = gain / loss
        rsi = RSI_MAX - (RSI_MAX / (1 + rs))
        return rsi.iloc[-1]
