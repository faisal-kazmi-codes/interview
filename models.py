from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    first_name = db.Column(db.String(250),  nullable=False)
    last_name=db.Column(db.String(250),  nullable=False)
    phone_number=db.Column(db.String(250), unique=True, nullable=True)
    password = db.Column(db.String(250), nullable=False)

    def __init__(self, email, first_name, last_name, phone_number,password):
            self.email = email
            self.first_name = first_name
            self.last_name = last_name
            self.phone_number = phone_number
            self.password = password