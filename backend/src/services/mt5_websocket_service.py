"""
MT5 WebSocket Service for MarketEdgePros
Handles real-time data streaming from MT5 via WebSocket
"""
import asyncio
import websockets
import json
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

class MT5WebSocketService:
    """Service for handling MT5 WebSocket real-time data streams"""
    
    def __init__(self, db_session, socketio_instance):
        """
        Initialize WebSocket service
        
        Args:
            db_session: SQLAlchemy database session
            socketio_instance: Socket.IO instance for frontend updates
        """
        self.ws_url = "ws://57.129.52.174:6710/ws"
        self.db = db_session
        self.socketio = socketio_instance
        self.connections = {}
        self.running = False
        self.reconnect_delay = 1
        self.max_reconnect_delay = 300  # 5 minutes
    
    async def start(self):
        """Start all WebSocket connections"""
        self.running = True
        logger.info("Starting MT5 WebSocket service...")
        
        # Start all three streams concurrently
        await asyncio.gather(
            self.connect_deal_stream(),
            self.connect_account_stream(),
            self.connect_position_stream(),
            return_exceptions=True
        )
    
    async def stop(self):
        """Stop all WebSocket connections"""
        self.running = False
        logger.info("Stopping MT5 WebSocket service...")
        
        for name, ws in self.connections.items():
            try:
                await ws.close()
                logger.info(f"Closed {name} stream")
            except Exception as e:
                logger.error(f"Error closing {name} stream: {e}")
    
    async def connect_deal_stream(self):
        """Connect to deal/trade stream"""
        url = f"{self.ws_url}?type=deal"
        stream_name = "deal"
        
        while self.running:
            try:
                async with websockets.connect(url) as websocket:
                    self.connections[stream_name] = websocket
                    logger.info(f"✅ Connected to MT5 {stream_name} stream")
                    self.reconnect_delay = 1  # Reset delay on successful connection
                    
                    async for message in websocket:
                        try:
                            await self.handle_deal_update(message)
                        except Exception as e:
                            logger.error(f"Error processing deal message: {e}")
                            
            except Exception as e:
                logger.error(f"{stream_name} stream disconnected: {e}")
                if self.running:
                    logger.info(f"Reconnecting {stream_name} in {self.reconnect_delay}s...")
                    await asyncio.sleep(self.reconnect_delay)
                    self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)
    
    async def connect_account_stream(self):
        """Connect to account balance/equity stream"""
        url = f"{self.ws_url}?type=account"
        stream_name = "account"
        
        while self.running:
            try:
                async with websockets.connect(url) as websocket:
                    self.connections[stream_name] = websocket
                    logger.info(f"✅ Connected to MT5 {stream_name} stream")
                    self.reconnect_delay = 1
                    
                    async for message in websocket:
                        try:
                            await self.handle_account_update(message)
                        except Exception as e:
                            logger.error(f"Error processing account message: {e}")
                            
            except Exception as e:
                logger.error(f"{stream_name} stream disconnected: {e}")
                if self.running:
                    logger.info(f"Reconnecting {stream_name} in {self.reconnect_delay}s...")
                    await asyncio.sleep(self.reconnect_delay)
                    self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)
    
    async def connect_position_stream(self):
        """Connect to position updates stream"""
        url = f"{self.ws_url}?type=position"
        stream_name = "position"
        
        while self.running:
            try:
                async with websockets.connect(url) as websocket:
                    self.connections[stream_name] = websocket
                    logger.info(f"✅ Connected to MT5 {stream_name} stream")
                    self.reconnect_delay = 1
                    
                    async for message in websocket:
                        try:
                            await self.handle_position_update(message)
                        except Exception as e:
                            logger.error(f"Error processing position message: {e}")
                            
            except Exception as e:
                logger.error(f"{stream_name} stream disconnected: {e}")
                if self.running:
                    logger.info(f"Reconnecting {stream_name} in {self.reconnect_delay}s...")
                    await asyncio.sleep(self.reconnect_delay)
                    self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)
    
    async def handle_deal_update(self, message: str):
        """
        Process deal/trade update from WebSocket
        
        Args:
            message: JSON string with deal data
        """
        try:
            data = json.loads(message)
            
            # Import models here to avoid circular imports
            from src.models.mt5_models import MT5Account, MT5Trade
            
            # Find account by MT5 login
            mt5_login = data.get('login')
            account = self.db.query(MT5Account).filter_by(mt5_login=str(mt5_login)).first()
            
            if not account:
                logger.warning(f"Received deal for unknown account: {mt5_login}")
                return
            
            ticket = data.get('ticket')
            
            # Check if trade already exists
            trade = self.db.query(MT5Trade).filter_by(ticket=ticket).first()
            
            if not trade:
                # Create new trade
                trade = MT5Trade(
                    mt5_account_id=account.id,
                    ticket=ticket,
                    symbol=data.get('symbol'),
                    trade_type=data.get('type', 'buy').lower(),
                    volume=data.get('volume', 0),
                    open_price=data.get('price', 0),
                    stop_loss=data.get('sl', 0),
                    take_profit=data.get('tp', 0),
                    open_time=datetime.fromisoformat(data.get('time')) if data.get('time') else datetime.utcnow(),
                    status='open'
                )
                self.db.add(trade)
                logger.info(f"New trade opened: {ticket} for account {mt5_login}")
            else:
                # Update existing trade (close)
                trade.close_price = data.get('close_price', data.get('price'))
                trade.close_time = datetime.fromisoformat(data.get('close_time')) if data.get('close_time') else datetime.utcnow()
                trade.profit = data.get('profit', 0)
                trade.commission = data.get('commission', 0)
                trade.swap = data.get('swap', 0)
                trade.status = 'closed'
                trade.updated_at = datetime.utcnow()
                logger.info(f"Trade closed: {ticket} for account {mt5_login}")
            
            self.db.commit()
            
            # Emit to frontend via Socket.IO
            self.socketio.emit('trade_update', {
                'user_id': account.user_id,
                'trade': trade.to_dict()
            }, room=f"user_{account.user_id}")
            
            # Trigger challenge progress calculation if linked to challenge
            if account.challenge_id:
                await self.calculate_challenge_progress(account.challenge_id)
            
        except Exception as e:
            logger.error(f"Failed to process deal update: {e}")
            self.db.rollback()
    
    async def handle_account_update(self, message: str):
        """
        Process account balance/equity update from WebSocket
        
        Args:
            message: JSON string with account data
        """
        try:
            data = json.loads(message)
            
            from src.models.mt5_models import MT5Account
            
            mt5_login = data.get('login')
            account = self.db.query(MT5Account).filter_by(mt5_login=str(mt5_login)).first()
            
            if not account:
                logger.warning(f"Received account update for unknown account: {mt5_login}")
                return
            
            # Update account data
            account.balance = data.get('balance', account.balance)
            account.equity = data.get('equity', account.equity)
            account.margin = data.get('margin', account.margin)
            account.free_margin = data.get('free_margin', account.free_margin)
            account.margin_level = data.get('margin_level', account.margin_level)
            account.updated_at = datetime.utcnow()
            
            self.db.commit()
            
            # Emit to frontend
            self.socketio.emit('account_update', {
                'user_id': account.user_id,
                'account': account.to_dict()
            }, room=f"user_{account.user_id}")
            
            logger.debug(f"Account updated: {mt5_login} - Balance: {account.balance}, Equity: {account.equity}")
            
        except Exception as e:
            logger.error(f"Failed to process account update: {e}")
            self.db.rollback()
    
    async def handle_position_update(self, message: str):
        """
        Process position update from WebSocket
        
        Args:
            message: JSON string with position data
        """
        try:
            data = json.loads(message)
            
            from src.models.mt5_models import MT5Account, MT5Position
            
            mt5_login = data.get('login')
            account = self.db.query(MT5Account).filter_by(mt5_login=str(mt5_login)).first()
            
            if not account:
                logger.warning(f"Received position update for unknown account: {mt5_login}")
                return
            
            ticket = data.get('ticket')
            
            # Check if position exists
            position = self.db.query(MT5Position).filter_by(ticket=ticket).first()
            
            if data.get('action') == 'close' and position:
                # Position closed, delete it
                self.db.delete(position)
                logger.info(f"Position closed and removed: {ticket}")
            else:
                if not position:
                    # Create new position
                    position = MT5Position(
                        mt5_account_id=account.id,
                        ticket=ticket,
                        symbol=data.get('symbol'),
                        position_type=data.get('type', 'buy').lower(),
                        volume=data.get('volume', 0),
                        price_open=data.get('price_open', 0),
                        price_current=data.get('price_current', 0),
                        stop_loss=data.get('sl', 0),
                        take_profit=data.get('tp', 0),
                        profit=data.get('profit', 0),
                        swap=data.get('swap', 0),
                        commission=data.get('commission', 0),
                        open_time=datetime.fromisoformat(data.get('time')) if data.get('time') else datetime.utcnow()
                    )
                    self.db.add(position)
                    logger.info(f"New position opened: {ticket}")
                else:
                    # Update existing position
                    position.price_current = data.get('price_current', position.price_current)
                    position.profit = data.get('profit', position.profit)
                    position.swap = data.get('swap', position.swap)
                    position.stop_loss = data.get('sl', position.stop_loss)
                    position.take_profit = data.get('tp', position.take_profit)
                    position.updated_at = datetime.utcnow()
                    logger.debug(f"Position updated: {ticket}")
            
            self.db.commit()
            
            # Emit to frontend
            self.socketio.emit('position_update', {
                'user_id': account.user_id,
                'position': position.to_dict() if position else {'ticket': ticket, 'action': 'closed'}
            }, room=f"user_{account.user_id}")
            
        except Exception as e:
            logger.error(f"Failed to process position update: {e}")
            self.db.rollback()
    
    async def calculate_challenge_progress(self, challenge_id: int):
        """
        Calculate and update challenge progress
        
        Args:
            challenge_id: Challenge ID to calculate progress for
        """
        try:
            # Import here to avoid circular imports
            from src.services.challenge_tracker_service import challenge_tracker
            await challenge_tracker.calculate_progress(challenge_id)
        except Exception as e:
            logger.error(f"Failed to calculate challenge progress for {challenge_id}: {e}")


# Global instance (will be initialized in app.py)
mt5_websocket_service: Optional[MT5WebSocketService] = None

def init_mt5_websocket_service(db_session, socketio_instance):
    """
    Initialize the MT5 WebSocket service
    
    Args:
        db_session: SQLAlchemy database session
        socketio_instance: Socket.IO instance
        
    Returns:
        MT5WebSocketService instance
    """
    global mt5_websocket_service
    mt5_websocket_service = MT5WebSocketService(db_session, socketio_instance)
    return mt5_websocket_service
