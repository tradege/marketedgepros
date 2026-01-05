"""
User Schemas
"""
from marshmallow import Schema, fields, validate


class UpdateProfileSchema(Schema):
    """Update user profile schema"""
    first_name = fields.Str(
        validate=validate.Length(min=1, max=100),
        allow_none=True
    )
    last_name = fields.Str(
        validate=validate.Length(min=1, max=100),
        allow_none=True
    )
    phone = fields.Str(
        validate=validate.Length(min=8, max=20),
        allow_none=True
    )
    country_code = fields.Str(
        validate=validate.Length(equal=2),
        allow_none=True
    )
    date_of_birth = fields.Date(allow_none=True)


class ChangePasswordSchema(Schema):
    """Change password schema"""
    current_password = fields.Str(required=True)
    new_password = fields.Str(
        required=True,
        validate=validate.Length(min=8, max=128)
    )
