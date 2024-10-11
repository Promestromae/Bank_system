from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from bank import bank_blueprint
from models import db

app = Flask(__name__)
app.register_blueprint(bank_blueprint)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
@app.route('/')
def home():
    return "Welcome to the Excity Bank!"

if __name__ == '__main__':
    app.run(debug=True)