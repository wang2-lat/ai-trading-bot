import pytest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
from analyzer import TechnicalAnalyzer
from risk_manager import RiskManager
from market_data import MarketData


class TestTechnicalAnalyzer:
    def test_analyze_stock_insufficient_data(self):
        analyzer = TechnicalAnalyzer()
        result = analyzer.analyze_stock(
            'TEST', 100, pd.DataFrame(), None, {}
        )
        assert result['action'] == 'HOLD'
        assert result['confidence'] == 0

    def test_calculate_rsi_normal(self):
        analyzer = TechnicalAnalyzer()
        prices = pd.Series([100, 102, 101, 103, 105, 104, 106, 108, 107, 109,
                           111, 110, 112, 114, 113, 115, 117, 116, 118, 120])
        rsi = analyzer._calculate_rsi(prices)
        assert 0 <= rsi <= 100

    def test_calculate_rsi_zero_loss(self):
        analyzer = TechnicalAnalyzer()
        # All increasing prices - zero loss
        prices = pd.Series([100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
                           110, 111, 112, 113, 114, 115, 116, 117, 118, 119])
        rsi = analyzer._calculate_rsi(prices)
        assert rsi == 100

    def test_analyze_stock_buy_signal(self):
        analyzer = TechnicalAnalyzer()
        # Create mock data with oversold condition
        historical_data = pd.DataFrame({
            'close': [100, 95, 90, 85, 80, 82, 84, 86, 88, 90,
                     92, 94, 96, 98, 100, 102, 104, 106, 108, 110]
        })
        result = analyzer.analyze_stock(
            'TEST', 110, historical_data, None, {'cash': 10000, 'position_count': 0}
        )
        assert result['action'] in ['BUY', 'HOLD']


class TestRiskManager:
    def test_calculate_position_size(self):
        mock_account = Mock()
        mock_account.portfolio_value = '100000'
        mock_account.cash = '50000'

        risk_manager = RiskManager(mock_account)
        shares = risk_manager.calculate_position_size('TEST', 100)

        # Should be 20% of portfolio / price
        expected = int(100000 * 0.20 / 100)
        assert shares == expected

    def test_calculate_position_size_insufficient_cash(self):
        mock_account = Mock()
        mock_account.portfolio_value = '100000'
        mock_account.cash = '1000'

        risk_manager = RiskManager(mock_account)
        shares = risk_manager.calculate_position_size('TEST', 200)

        # Should be limited by cash
        assert shares == 5

    def test_check_stop_loss_triggered(self):
        mock_account = Mock()
        mock_account.portfolio_value = '100000'
        mock_account.cash = '50000'

        mock_position = Mock()
        mock_position.symbol = 'TEST'
        mock_position.avg_entry_price = '100'
        mock_position.current_price = '94'  # 6% loss
        mock_position.qty = '10'

        risk_manager = RiskManager(mock_account)
        signals = risk_manager.check_stop_loss([mock_position])

        assert len(signals) == 1
        assert signals[0]['symbol'] == 'TEST'

    def test_check_stop_loss_not_triggered(self):
        mock_account = Mock()
        mock_account.portfolio_value = '100000'
        mock_account.cash = '50000'

        mock_position = Mock()
        mock_position.symbol = 'TEST'
        mock_position.avg_entry_price = '100'
        mock_position.current_price = '98'  # 2% loss
        mock_position.qty = '10'

        risk_manager = RiskManager(mock_account)
        signals = risk_manager.check_stop_loss([mock_position])

        assert len(signals) == 0

    def test_can_open_position_at_limit(self):
        mock_account = Mock()
        mock_account.portfolio_value = '100000'
        mock_account.cash = '50000'

        risk_manager = RiskManager(mock_account)
        assert risk_manager.can_open_position(5) == False
        assert risk_manager.can_open_position(4) == True


class TestMarketData:
    @patch('market_data.tradeapi.REST')
    def test_is_market_open(self, mock_rest):
        mock_api = Mock()
        mock_clock = Mock()
        mock_clock.is_open = True
        mock_api.get_clock.return_value = mock_clock
        mock_rest.return_value = mock_api

        market_data = MarketData()
        assert market_data.is_market_open() == True

    @patch('market_data.tradeapi.REST')
    def test_is_market_closed(self, mock_rest):
        mock_api = Mock()
        mock_clock = Mock()
        mock_clock.is_open = False
        mock_api.get_clock.return_value = mock_clock
        mock_rest.return_value = mock_api

        market_data = MarketData()
        assert market_data.is_market_open() == False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
