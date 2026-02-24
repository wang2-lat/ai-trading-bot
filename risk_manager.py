import config
from logger import logger

class RiskManager:
    def __init__(self, account):
        self.account = account
        self.portfolio_value = float(account.portfolio_value)
        self.cash = float(account.cash)

    def check_stop_loss(self, positions):
        """Check if any position needs stop loss"""
        stop_loss_signals = []

        for position in positions:
            cost_basis = float(position.avg_entry_price)
            current_price = float(position.current_price)
            pnl_percent = (current_price - cost_basis) / cost_basis

            if pnl_percent <= -config.STOP_LOSS_PCT:
                logger.warning(f"STOP LOSS triggered for {position.symbol}: {pnl_percent*100:.2f}%")
                stop_loss_signals.append({
                    'symbol': position.symbol,
                    'qty': position.qty,
                    'pnl_percent': pnl_percent * 100
                })

        return stop_loss_signals

    def calculate_position_size(self, symbol, current_price):
        """Calculate how many shares to buy"""
        max_position_value = self.portfolio_value * config.POSITION_SIZE_PCT
        max_shares = int(max_position_value / current_price)

        # Check if we have enough cash
        required_cash = max_shares * current_price
        if required_cash > self.cash:
            max_shares = int(self.cash / current_price)

        logger.info(f"Position size for {symbol}: {max_shares} shares (${max_shares * current_price:.2f})")
        return max_shares

    def can_open_position(self, current_position_count):
        """Check if we can open a new position"""
        if current_position_count >= config.MAX_POSITIONS:
            logger.warning(f"Cannot open new position: already at max ({config.MAX_POSITIONS})")
            return False
        return True

    def get_position_info(self, symbol, positions):
        """Get position info for a specific symbol"""
        for position in positions:
            if position.symbol == symbol:
                cost_basis = float(position.avg_entry_price)
                current_price = float(position.current_price)
                pnl_percent = (current_price - cost_basis) / cost_basis * 100

                return {
                    'cost_basis': cost_basis,
                    'current_price': current_price,
                    'pnl_percent': pnl_percent,
                    'qty': position.qty
                }
        return None
