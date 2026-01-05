"""
Schema Validation Decorator
"""
from functools import wraps
from flask import request, jsonify
from marshmallow import ValidationError


def validate_schema(schema_class):
    """
    Decorator to validate request data against a Marshmallow schema
    
    Usage:
        @validate_schema(RegisterSchema)
        def register():
            data = request.validated_data
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            schema = schema_class()
            
            try:
                # Get JSON data from request
                json_data = request.get_json()
                
                if json_data is None:
                    return jsonify({'error': 'No JSON data provided'}), 400
                
                # Validate and deserialize
                validated_data = schema.load(json_data)
                
                # Attach validated data to request object
                request.validated_data = validated_data
                
                # Call the original function
                return f(*args, **kwargs)
                
            except ValidationError as e:
                # Return validation errors
                return jsonify({
                    'error': 'Validation failed',
                    'errors': e.messages
                }), 400
            except Exception as e:
                # Catch other errors
                return jsonify({
                    'error': 'Invalid request data'
                }), 400
        
        return decorated_function
    return decorator
