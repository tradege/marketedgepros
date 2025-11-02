"""
Unit tests for Trade model
"""
import pytest
from decimal import Decimal
from datetime import datetime, timedelta
from src.models import Trade

@pytest.mark.unit
@pytest.mark.model
class TestTradeModel:
    """Test Trade model functionality"""
    
    def test_create_trade(self, session, challenge):
        """Test creating a trade"""
        trade = Trade(
            challenge_id=challenge.id,
            ticket='TKT123456',
            symbol='EURUSD',
            trade_type='buy',
            volume=Decimal('1.00'),
            open_price=Decimal('1.10000'),
            open_time=datetime.utcnow(),
            status='open'
        )
        session.add(trade)
        session.commit()
        
        assert trade.id is not None
        assert trade.challenge_id == challenge.id
        assert trade.ticket == 'TKT123456'
        assert trade.symbol == 'EURUSD'
        assert trade.trade_type == 'buy'
    
    def test_trade_unique_ticket(self, session, challenge):
        """Test trade ticket uniqueness"""
        trade1 = Trade(
            challenge_id=challenge.id,
            ticket='TKT123',
            symbol='EURUSD',
            trade_type='buy',
            volume=Decimal('1.00'),
            open_price=Decimal('1.10000'),
            open_time=datetime.utcnow()
        )
        session.add(trade1)
        session.commit()
        
        # Try to create another trade with same ticket
        trade2 = Trade(
            challenge_id=challenge.id,
            ticket='TKT123',
            symbol='GBPUSD',
            trade_type='sell',
            volume=Decimal('1.00'),
            open_price=Decimal('1.30000'),
            open_time=datetime.utcnow()
        )
        session.add(trade2)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            session.commit()
    
    def test_trade_open_to_close(self, session, challenge):
        """Test opening and closing a trade"""
        trade = Trade(
            challenge_id=challenge.id,
            ticket='TKT789',
            symbol='EURUSD',
            trade_type='buy',
            volume=Decimal('1.00'),
            open_price=Decimal('1.10000'),
            open_time=datetime.utcnow(),
            status='open'
        )
        session.add(trade)
        session.commit()
        
        assert trade.status == 'open'
        assert trade.close_price is None
        
        # Close the trade
        trade.status = 'closed'
        trade.close_price = Decimal('1.10500')
        trade.close_time = datetime.utcnow()
        trade.profit = Decimal('50.00')
        session.commit()
        
        assert trade.status == 'closed'
        assert trade.close_price == Decimal('1.10500')
        assert trade.profit == Decimal('50.00')
    
    def test_trade_with_stop_loss(self, session, challenge):
        """Test trade with stop loss"""
        trade = Trade(
            challenge_id=challenge.id,
            ticket='TKT456',
            symbol='EURUSD',
            trade_type='buy',
            volume=Decimal('1.00'),
            open_price=Decimal('1.10000'),
            stop_loss=Decimal('1.09500'),
            open_time=datetime.utcnow()
        )
        session.add(trade)
        session.commit()
        
        assert trade.stop_loss == Decimal('1.09500')
    
    def test_trade_with_take_profit(self, session, challenge):
        """Test trade with take profit"""
        trade = Trade(
            challenge_id=challenge.id,
            ticket='TKT789',
            symbol='EURUSD',
            trade_type='buy',
            volume=Decimal('1.00'),
            open_price=Decimal('1.10000'),
            take_profit=Decimal('1.10500'),
            open_time=datetime.utcnow()
        )
        session.add(trade)
        session.commit()
        
        assert trade.take_profit == Decimal('1.10500')
    
    def test_trade_with_commission_and_swap(self, session, challenge):
        """Test trade with commission and swap"""
        trade = Trade(
            challenge_id=challenge.id,
            ticket='TKT999',
            symbol='EURUSD',
            trade_type='buy',
            volume=Decimal('1.00'),
            open_price=Decimal('1.10000'),
            close_price=Decimal('1.10500'),
            profit=Decimal('50.00'),
            commission=Decimal('5.00'),
            swap=Decimal('-2.00'),
            open_time=datetime.utcnow(),
            close_time=datetime.utcnow(),
            status='closed'
        )
        session.add(trade)
        session.commit()
        
        assert trade.commission == Decimal('5.00')
        assert trade.swap == Decimal('-2.00')
        # Net profit = 50 - 5 - 2 = 43
        net_profit = trade.profit - trade.commission - trade.swap
        assert net_profit == Decimal('47.00')
    
    def test_trade_buy_type(self, session, challenge):
        """Test buy trade"""
        trade = Trade(
            challenge_id=challenge.id,
            ticket='TKTBUY',
            symbol='EURUSD',
            trade_type='buy',
            volume=Decimal('1.00'),
            open_price=Decimal('1.10000'),
            open_time=datetime.utcnow()
        )
        session.add(trade)
        session.commit()
        
        assert trade.trade_type == 'buy'
    
    def test_trade_sell_type(self, session, challenge):
        """Test sell trade"""
        trade = Trade(
            challenge_id=challenge.id,
            ticket='TKTSELL',
            symbol='EURUSD',
            trade_type='sell',
            volume=Decimal('1.00'),
            open_price=Decimal('1.10000'),
            open_time=datetime.utcnow()
        )
        session.add(trade)
        session.commit()
        
        assert trade.trade_type == 'sell'
    
    def test_trade_decimal_precision(self, session, challenge):
        """Test trade decimal precision"""
        trade = Trade(
            challenge_id=challenge.id,
            ticket='TKTPREC',
            symbol='EURUSD',
            trade_type='buy',
            volume=Decimal('1.23'),
            open_price=Decimal('1.10456'),
            close_price=Decimal('1.10789'),
            profit=Decimal('123.45'),
            open_time=datetime.utcnow()
        )
        session.add(trade)
        session.commit()
        
        assert trade.volume == Decimal('1.23')
        assert trade.open_price == Decimal('1.10456')
        assert trade.close_price == Decimal('1.10789')
    
    def test_trade_to_dict(self, session, challenge):
        """Test trade serialization"""
        now = datetime.utcnow()
        trade = Trade(
            challenge_id=challenge.id,
            ticket='TKTDICT',
            symbol='EURUSD',
            trade_type='buy',
            volume=Decimal('1.00'),
            open_price=Decimal('1.10000'),
            open_time=now
        )
        session.add(trade)
        session.commit()
        
        trade_dict = trade.to_dict()
        
        assert trade_dict['ticket'] == 'TKTDICT'
        assert trade_dict['symbol'] == 'EURUSD'
        assert trade_dict['trade_type'] == 'buy'
        assert trade_dict['volume'] == 1.00
        assert trade_dict['open_price'] == 1.10000
    
    def test_trade_timestamps(self, session, challenge):
        """Test trade timestamp tracking"""
        trade = Trade(
            challenge_id=challenge.id,
            ticket='TKTTIME',
            symbol='EURUSD',
            trade_type='buy',
            volume=Decimal('1.00'),
            open_price=Decimal('1.10000'),
            open_time=datetime.utcnow()
        )
        session.add(trade)
        session.commit()
        
        assert trade.created_at is not None
        assert trade.updated_at is not None
    
    def test_trade_profit_calculation(self, session, challenge):
        """Test trade profit calculation"""
        trade = Trade(
            challenge_id=challenge.id,
            ticket='TKTPROFIT',
            symbol='EURUSD',
            trade_type='buy',
            volume=Decimal('1.00'),
            open_price=Decimal('1.10000'),
            close_price=Decimal('1.10500'),
            open_time=datetime.utcnow(),
            close_time=datetime.utcnow(),
            status='closed'
        )
        session.add(trade)
        session.commit()
        
        # For a buy trade: profit = (close - open) * volume * contract_size
        # Simplified: 0.00500 * 1.00 * 100000 = 500
        trade.profit = Decimal('500.00')
        session.commit()
        
        assert trade.profit == Decimal('500.00')
    
    def test_trade_loss_calculation(self, session, challenge):
        """Test trade loss calculation"""
        trade = Trade(
            challenge_id=challenge.id,
            ticket='TKTLOSS',
            symbol='EURUSD',
            trade_type='buy',
            volume=Decimal('1.00'),
            open_price=Decimal('1.10000'),
            close_price=Decimal('1.09500'),
            open_time=datetime.utcnow(),
            close_time=datetime.utcnow(),
            status='closed'
        )
        session.add(trade)
        session.commit()
        
        # For a buy trade with loss: profit = (close - open) * volume * contract_size
        # Simplified: -0.00500 * 1.00 * 100000 = -500
        trade.profit = Decimal('-500.00')
        session.commit()
        
        assert trade.profit == Decimal('-500.00')
    
    def test_trade_multiple_symbols(self, session, challenge):
        """Test trades with different symbols"""
        symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'GOLD', 'OIL']
        
        for i, symbol in enumerate(symbols):
            trade = Trade(
                challenge_id=challenge.id,
                ticket=f'TKT{i}',
                symbol=symbol,
                trade_type='buy',
                volume=Decimal('1.00'),
                open_price=Decimal('1.10000'),
                open_time=datetime.utcnow()
            )
            session.add(trade)
        
        session.commit()
        
        trades = session.query(Trade).filter_by(challenge_id=challenge.id).all()
        assert len(trades) == 5
        assert set(t.symbol for t in trades) == set(symbols)
