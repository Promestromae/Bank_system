from flask import Blueprint, request, jsonify
from models import session, BankAccount, Transaction  # Import your SQLAlchemy session and models

bank_bp = Blueprint('bank', __name__)

@bank_bp.route('/accounts', methods=['POST'])
def create_account():
    data = request.get_json()
    user_id = data['user_id']  # Assuming accounts are associated with a user
    account_number = data['account_number']

    # Check if account already exists
    if session.query(BankAccount).filter_by(account_number=account_number).first():
        return jsonify({'message': 'Account already exists'}), 400

    # Create new bank account
    new_account = BankAccount(user_id=user_id, account_number=account_number)
    session.add(new_account)
    session.commit()

    return jsonify({'message': 'Account created successfully', 'account_id': new_account.id}), 201

@bank_bp.route('/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    account = session.query(BankAccount).get(account_id)
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
    account_id = data['account_id']
    amount = data['amount']
    transaction_type = data['transaction_type']  # e.g., 'deposit' or 'withdrawal'

    # Validate input
    if amount <= 0:
        return jsonify({'message': 'Amount must be greater than zero'}), 400

    account = session.query(BankAccount).get(account_id)
    if not account:
        return jsonify({'message': 'Account not found'}), 404

    # Handle deposit and withdrawal
    if transaction_type == 'deposit':
        account.balance += amount
    elif transaction_type == 'withdrawal':
        if account.balance < amount:
            return jsonify({'message': 'Insufficient balance'}), 400
        account.balance -= amount
    else:
        return jsonify({'message': 'Invalid transaction type'}), 400

    # Record the transaction
    transaction = Transaction(account_id=account_id, amount=amount, transaction_type=transaction_type)
    session.add(transaction)
    session.commit()

    return jsonify({
        'message': 'Transaction successful',
        'new_balance': account.balance
    }), 201

@bank_bp.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = session.query(Transaction).all()
    return jsonify([{
        'account_id': t.account_id,
        'amount': t.amount,
        'transaction_type': t.transaction_type,
        'timestamp': t.timestamp.isoformat()  # Format timestamp to ISO string
    } for t in transactions]), 200
