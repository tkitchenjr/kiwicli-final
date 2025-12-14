import pytest
import app.services.transaction_services as transaction_services
from app.domain.Transactions import Transactions
from app.services.transaction_services import update_transaction_record, view_transactions
from datetime import datetime

def test_update_transaction_record(db_session, monkeypatch):
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)

    result = update_transaction_record(transaction_id='2', user_id='user1', portfolio_id='port1', security_id='sec1', transaction_type='BUY', qty=10, price=100.0, timestamp='provided')
    
    assert result is None
    assert db_session.query(Transactions).count() == 1

def test_update_transaction_record_buy(db_session, monkeypatch):
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)

    update_transaction_record(transaction_id='2', user_id='user1', portfolio_id='port1', security_id='sec1', transaction_type='BUY', qty=10, price=100.0, timestamp='provided')

    transaction = db_session.query(Transactions).filter_by(transaction_id='2').first()
    assert transaction is not None
    assert transaction.transaction_type == 'BUY'
   
def test_update_transaction_record_sell(db_session, monkeypatch):
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)

    update_transaction_record(transaction_id='2', user_id='user1', portfolio_id='port1', security_id='sec1', transaction_type='SELL', qty=10, price=100.0, timestamp='provided')

    transaction = db_session.query(Transactions).filter_by(transaction_id='2').first()
    assert transaction is not None
    assert transaction.transaction_type == 'SELL'
    
def test_update_transaction_record_negative_qty(db_session, monkeypatch):
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)

    update_transaction_record(transaction_id='3', user_id='user1', portfolio_id='port1', security_id='sec1', transaction_type='SELL', qty=-5, price=50.0, timestamp='provided')

    transaction = db_session.query(Transactions).filter_by(transaction_id='3').first()
    assert transaction is not None
    assert transaction.qty == -5

def test_view_transactions(db_session, monkeypatch):
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)

    update_transaction_record(transaction_id='2', user_id='user1', portfolio_id='port1', security_id='sec1', transaction_type='BUY', qty=10, price=100.0, timestamp='provided')

    result = view_transactions()

    assert result is None
    assert db_session.query(Transactions).count() == 1

def test_view_transactions_no_transactions(db_session, monkeypatch):
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)

    result = view_transactions()
    
    assert result is None
    assert db_session.query(Transactions).count() == 0

def test_query_transactions_by_user_empty(db_session, monkeypatch):
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)

    result = transaction_services.query_transactions_by_user('')
    assert result is None

def test_query_by_user(db_session, monkeypatch):
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)

    update_transaction_record(transaction_id='2', user_id='user1', portfolio_id='port1', security_id='sec1', transaction_type='BUY', qty=10, price=100.0, timestamp='provided')
    update_transaction_record(transaction_id='3', user_id='user2', portfolio_id='port2', security_id='sec2', transaction_type='SELL', qty=5, price=200.0, timestamp='provided')

    transactions_user1 = db_session.query(Transactions).filter_by(user_id='user1').all()
    transactions_user2 = db_session.query(Transactions).filter_by(user_id='user2').all()

    assert len(transactions_user1) == 1
    assert transactions_user1[0].transaction_type == 'BUY'
    assert len(transactions_user2) == 1
    assert transactions_user2[0].transaction_type == 'SELL'

def test_query_by_security(db_session, monkeypatch):
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)

    update_transaction_record(transaction_id='2', user_id='user1', portfolio_id='port1', security_id='AAPL', transaction_type='BUY', qty=10, price=100.0, timestamp='provided')
    update_transaction_record(transaction_id='3', user_id='user2', portfolio_id='port2', security_id='MSFT', transaction_type='SELL', qty=5, price=200.0, timestamp='provided')

    transactions_sec1 = db_session.query(Transactions).filter_by(security_id='AAPL').all()
    transactions_sec2 = db_session.query(Transactions).filter_by(security_id='MSFT').all()

    assert len(transactions_sec1) == 1
    assert transactions_sec1[0].user_id == 'user1'
    assert len(transactions_sec2) == 1
    assert transactions_sec2[0].user_id == 'user2'

def test_query_by_portfolio(db_session, monkeypatch):
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)

    update_transaction_record(transaction_id='2', user_id='user1', portfolio_id='port1', security_id='sec1', transaction_type='BUY', qty=10, price=100.0, timestamp='provided')
    update_transaction_record(transaction_id='3', user_id='user2', portfolio_id='port2', security_id='sec2', transaction_type='SELL', qty=5, price=200.0, timestamp='provided')

    transactions_port1 = db_session.query(Transactions).filter_by(portfolio_id='port1').all()
    transactions_port2 = db_session.query(Transactions).filter_by(portfolio_id='port2').all()

    assert len(transactions_port1) == 1
    assert transactions_port1[0].user_id == 'user1'
    assert len(transactions_port2) == 1
    assert transactions_port2[0].user_id == 'user2'

def test_query_by_portfolio_portfolio_not_found(db_session, monkeypatch):
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)

    update_transaction_record(transaction_id='2', user_id='user1', portfolio_id='port1', security_id='sec1', transaction_type='BUY', qty=10, price=100.0, timestamp='provided')

    transactions_port3 = db_session.query(Transactions).filter_by(portfolio_id='port3').all()

    assert len(transactions_port3) == 0

def test_query_by_portfolio_empty(db_session, monkeypatch):
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)

    transactions_port_empty = db_session.query(Transactions).filter_by(portfolio_id='').all()

    assert len(transactions_port_empty) == 0

def test_query_by_portfolio_no_transactions(db_session, monkeypatch):
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)

    transactions_port1 = db_session.query(Transactions).filter_by(portfolio_id='port1').all()

    assert len(transactions_port1) == 0

def test_query_by_portfolio_invalid_id(db_session, monkeypatch):
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)

    transactions_port_invalid = db_session.query(Transactions).filter_by(portfolio_id='').all()

    assert len(transactions_port_invalid) == 0

def test_query_transactions_by_security_not_found(db_session, monkeypatch):
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)

    result = transaction_services.query_transactions_by_security('NONE')
    assert result is None
