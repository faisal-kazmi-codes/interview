from marshmallow import Schema, fields, validate, ValidationError

class UserSchema:
    user_register = Schema.from_dict({
    "email": fields.Email(required=True),
    "first_name": fields.Str(required=True, validate=validate.Length(min=1)),
    "last_name": fields.Str(required=True, validate=validate.Length(min=1)),
    "phone_number": fields.Str(required=False),
    "password": fields.Str(required=True, validate=validate.Length(min=6)),
    })

    user_login = Schema.from_dict({
    "email_id" : fields.Email(required=True),
    "password" : fields.Str(required=True),
    
   })