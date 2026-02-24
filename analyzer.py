import pandas as pd
import config
from logger import logger

class TechnicalAnalyzer:
    def analyze_stock(self, symbol, current_price, historical_data, position_info, account_info):
        """Analyze stock using technical indicators"""

        if historical_data.empty or len(historical_data) < 20:
            logger.warning(f"Insufficient data for {symbol}")
            return {"action": "HOLD", "confidence": 0, "reason": "Insufficient data"}

        try:
            # Calculate indicators
            rsi = self._calculate_rsi(historical_data['close'])
            sma_short = historical_data['close'].rolling(5).mean().iloc[-1]
            sma_long = historical_data['close'].rolling(20).mean().iloc[-1]

            # Determine action
            action = "HOLD"
            confidence = 50
            reason = ""

            is_holding = position_info is not None

            # BUY signals
            if not is_holding and rsi < 30 and current_price > sma_short > sma_long:
                action = "BUY"
                confidence = 75
                reason = f"Oversold (RSI={rsi:.1f}) with uptrend"
            elif not is_holding and current_price > sma_short and sma_short > sma_long:
                action = "BUY"
                confidence = 65
                reason = "Strong uptrend"

            # SELL signals
            elif is_holding and rsi > 70:
                action = "SELL"
                confidence = 80
                reason = f"Overbought (RSI={rsi:.1f})"
            elif is_holding and current_price < sma_short < sma_long:
                action = "SELL"
                confidence = 70
                reason = "Downtrend detected"

            logger.info(f"{symbol}: {action} (confidence: {confidence}%) - {reason}")
            return {"action": action, "confidence": confidence, "reason": reason}

        except Exception as e:
            logger.error(f"Technical analysis failed for {symbol}: {e}")
            return {"action": "HOLD", "confidence": 0, "reason": "Analysis error"}

    def _calculate_rsi(self, prices, period=14):
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()

        # Avoid division by zero
        if loss.iloc[-1] == 0:
            return 100 if gain.iloc[-1] > 0 else 50

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1]
