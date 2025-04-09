from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import User , db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from config import Config
from schemas import UserSchema
from marshmallow import ValidationError

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
migrate=Migrate(app,db)


@app.route("/register", methods=['POST'])
def create_user():
    try:
        data = UserSchema.user_register().load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    email_id = data['email']
    if User.query.filter_by(email=email_id).first():
        return jsonify({'error': 'User with this email already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(
        email=email_id,
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        phone_number=data.get('phone_number'),
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    try:
        data = UserSchema.user_login().load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    user = User.query.filter_by(email=data.get['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token})
    else:
        return jsonify({'message': 'Invalid email or password'}), 401