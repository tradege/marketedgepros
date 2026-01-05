"""
Payment Schemas
"""
from marshmallow import Schema, fields, validate, validates, ValidationError


class CreatePaymentSchema(Schema):
    """Create payment schema"""
    challenge_id = fields.Int(required=True)
    amount = fields.Decimal(
        required=True,
        as_string=True,
        error_messages={'required': 'Amount is required'}
    )
    payment_method = fields.Str(
        required=True,
        validate=validate.OneOf(['credit_card', 'crypto', 'bank_transfer'])
    )
    currency = fields.Str(
        validate=validate.OneOf(['USD', 'EUR', 'GBP', 'USDT']),
        missing='USD'
    )
    
    @validates('amount')
    def validate_amount(self, value):
        """Validate amount is positive"""
        if value <= 0:
            raise ValidationError('Amount must be positive')


class PayoutRequestSchema(Schema):
    """Payout request schema"""
    amount = fields.Decimal(
        required=True,
        as_string=True
    )
    payment_method = fields.Str(
        required=True,
        validate=validate.OneOf(['bank_transfer', 'crypto', 'paypal'])
    )
    wallet_address = fields.Str(
        validate=validate.Length(max=200),
        allow_none=True
    )
    bank_account = fields.Str(
        validate=validate.Length(max=50),
        allow_none=True
    )
    
    @validates('amount')
    def validate_amount(self, value):
        """Validate amount"""
        if value <= 0:
            raise ValidationError('Amount must be positive')
        if value < 50:
            raise ValidationError('Minimum payout amount is $50')
