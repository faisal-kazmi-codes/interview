from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import User , db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
migrate=Migrate(app,db)

@app.route("/register",methods=['POST'])
def create_user():
    data = request.json
    email_id = data.get('email_id')
    first_name = data.get('first_name')
    last_name= data.get('last_name')
    phone_number=data.get('phone_number')
    password = data.get('password')
    if email_id and password:
        if User.query.filter_by(email_id=email_id).first():
            return jsonify({'error': 'User with this email or username already exists'})
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(email_id=email_id, first_name=first_name, last_name=last_name,
                    phone_number=phone_number, password=hashed_password)
        db.session.add(new_user)
        return jsonify({'message': 'User created successfully'})
    else:
        return jsonify({'error': 'All fields need to be provided'})
    
    
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email_id=data.get('email_id')
    password=data.get('password')
    user = User.query.filter_by(email_id=email_id).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token})
    else:
        return jsonify({'message': 'Invalid email or password'})