from flask import Blueprint, request, jsonify
from models import db, BankAccount, Transaction

bank_bp = Blueprint('bank', __name__)

@bank_bp.route('/accounts', methods=['POST'])
def create_account():
    data = request.get_json()
    user_id = data.get('user_id')
    account_number = data.get('account_number')

    if db.session.query(BankAccount).filter_by(account_number=account_number).first():
        return jsonify({'message': 'Account already exists'}), 400

    new_account = BankAccount(user_id=user_id, account_number=account_number)
    db.session.add(new_account)
    db.session.commit()

    return jsonify({'message': 'Account created successfully', 'account_id': new_account.id}), 201

@bank_bp.route('/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    account = db.session.query(BankAccount).get(account_id)
    if not account:
        return jsonify({'message': 'Account not found'}), 404

    return jsonify({
        'account_id': account.id,
        'account_number': account.account_number,
        'balance': account.balance
    }), 200

@bank_bp.route('/transactions', methods=['POST'])
def create_transaction():
    data = request.get_json()
    account_id = data.get('account_id')
    amount = data.get('amount')
    transaction_type = data.get('transaction_type')

    if amount <= 0:
        return jsonify({'message': 'Amount must be greater than zero'}), 400

    account = db.session.query(BankAccount).get(account_id)
    if not account:
        return jsonify({'message': 'Account not found'}), 404

    if transaction_type == 'deposit':
        account.balance += amount
    elif transaction_type == 'withdrawal':
        if account.balance < amount:
            return jsonify({'message': 'Insufficient balance'}), 400
        account.balance -= amount
    else:
        return jsonify({'message': 'Invalid transaction type'}), 400

    transaction = Transaction(account_id=account_id, amount=amount, transaction_type=transaction_type)
    db.session.add(transaction)
    db.session.commit()

    return jsonify({'message': 'Transaction successful', 'new_balance': account.balance}), 201

@bank_bp.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = db.session.query(Transaction).all()
    return jsonify([{
        'account_id': t.account_id,
        'amount': t.amount,
        'transaction_type': t.transaction_type,
        'timestamp': t.timestamp.isoformat()
    } for t in transactions]), 200
