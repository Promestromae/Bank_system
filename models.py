from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    
    accounts = relationship('BankAccount', back_populates='user')

class BankAccount(Base):
    __tablename__ = 'bank_accounts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    account_number = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=0.0)
    
    user = relationship('User', back_populates='accounts')
    transactions = relationship('Transaction', back_populates='account')

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('bank_accounts.id'), nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    transaction_type = Column(String, nullable=False)  # e.g., 'deposit', 'withdrawal'
    
    account = relationship('BankAccount', back_populates='transactions')

# Create an engine and a session
engine = create_engine('sqlite:///bank_system.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()