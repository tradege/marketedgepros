"""
Challenge Schemas
"""
from marshmallow import Schema, fields, validate, validates, ValidationError


class CreateChallengeSchema(Schema):
    """Create challenge schema"""
    program_id = fields.Int(required=True, error_messages={
        'required': 'Program ID is required'
    })
    account_size = fields.Decimal(
        required=True,
        as_string=True,
        error_messages={'required': 'Account size is required'}
    )
    payment_method = fields.Str(
        required=True,
        validate=validate.OneOf(['credit_card', 'crypto', 'bank_transfer']),
        error_messages={'required': 'Payment method is required'}
    )
    
    @validates('account_size')
    def validate_account_size(self, value):
        """Validate account size is positive"""
        if value <= 0:
            raise ValidationError('Account size must be positive')


class UpdateChallengeSchema(Schema):
    """Update challenge schema"""
    status = fields.Str(
        validate=validate.OneOf([
            'pending', 'active', 'passed', 'failed', 
            'breached', 'funded', 'cancelled'
        ]),
        allow_none=True
    )
    mt5_login = fields.Str(
        validate=validate.Length(max=50),
        allow_none=True
    )
    mt5_password = fields.Str(
        validate=validate.Length(max=50),
        allow_none=True
    )
    mt5_server = fields.Str(
        validate=validate.Length(max=100),
        allow_none=True
    )
