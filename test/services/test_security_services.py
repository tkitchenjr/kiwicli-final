import pytest
from app.domain.Security import Security
from app.domain.Portfolio import Portfolio
from app.domain.User import User
from app.domain.Investment import Investment
from app.services.security_services import place_order, view_all_securities

def test_view_all_securities(db_session, monkeypatch):
    monkeypatch.setattr('app.services.security_services.get_session', lambda: db_session)
    
    security1 = Security(symbol='AAPL', issuer='Apple Inc.', name='Apple Stock', price=150.0)
    security2 = Security(symbol='MSFT', issuer='Microsoft Corp.', name='Microsoft Stock', price=250.0)
    db_session.add(security1)
    db_session.add(security2)
    db_session.commit()
    
    result = view_all_securities()
    
    assert result is None
    assert db_session.query(Security).count() == 2

def test_view_all_securities_no_securities(db_session, monkeypatch):
    monkeypatch.setattr('app.services.security_services.get_session', lambda: db_session)
    
    result = view_all_securities()
    
    assert result is None
    assert db_session.query(Security).count() == 0

def test_place_order_success(db_session, monkeypatch):
    monkeypatch.setattr('app.services.security_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.login_services.current_user', 'testuser')
    
    user = User(username='testuser', password='password', firstname='First', lastname='Last', balance=10000)
    portfolio = Portfolio(id=1, name='Test Portfolio', description='Test Description', owner='testuser')
    security = Security(symbol='AAPL', issuer='Apple Inc.', name='Apple Stock', price=150.0)
    db_session.add(user)
    db_session.add(portfolio)
    db_session.add(security)
    db_session.commit()     

    result = place_order(portfolio_id=1, ticker='AAPL', quantity=10)    
    assert result == True
    updated_user = db_session.query(User).filter_by(username='testuser').first()
    assert updated_user.balance == 8500.0

def test_place_order_insufficient_funds(db_session, monkeypatch):
    monkeypatch.setattr('app.services.security_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.login_services.current_user', 'testuser')
    
    user = User(username='testuser', password='password', firstname='First', lastname='Last', balance=500)
    portfolio = Portfolio(id=1, name='Test Portfolio', description='Test Description', owner='testuser')
    security = Security(symbol='AAPL', issuer='Apple Inc.', name='Apple Stock', price=150.0)
    db_session.add(user)
    db_session.add(portfolio)
    db_session.add(security)
    db_session.commit() 

    result = place_order(portfolio_id=1, ticker='AAPL', quantity=10)
    assert result == False

def test_place_order_invalid_security(db_session, monkeypatch):
    monkeypatch.setattr('app.services.security_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.login_services.current_user', 'testuser')

    user = User(username='testuser', password='password', firstname='First', lastname='Last', balance=10000)
    portfolio = Portfolio(id=1, name='Test Portfolio', description='Test Description', owner='testuser')
    db_session.add(user)
    db_session.add(portfolio)
    db_session.commit()

    result = place_order(portfolio_id=1, ticker='INVALID', quantity=10)
    assert result == False

def test_place_order_insufficient_quantity(db_session, monkeypatch):
    monkeypatch.setattr('app.services.security_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.login_services.current_user', 'testuser')
    
    user = User(username='testuser', password='password', firstname='First', lastname='Last', balance=10000)
    portfolio = Portfolio(id=1, name='Test Portfolio', description='Test Description', owner='testuser')
    security = Security(symbol='AAPL', issuer='Apple Inc.', name='  Apple Stock', price=150.0)
    db_session.add(user)
    db_session.add(portfolio)
    db_session.add(security)
    db_session.commit() 

    result = place_order(portfolio_id=1, ticker='AAPL', quantity=-5)
    assert result == False

def test_place_order_add_to_existing_investment(db_session, monkeypatch):
    monkeypatch.setattr('app.services.security_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.login_services.current_user', 'testuser')
    
    user = User(username='testuser', password='password', firstname='First', lastname='Last', balance=10000)
    portfolio = Portfolio(id=1, name='Test Portfolio', description='Test Description', owner='testuser')
    security = Security(symbol='AAPL', issuer='Apple Inc.', name='Apple Stock', price=150.0)
    investment = Investment(portfolio_id=1, Ticker='AAPL', Qty=10, purchase_price=150.0)
    db_session.add(user)
    db_session.add(portfolio)
    db_session.add(security)
    db_session.add(investment)
    db_session.commit()     

    result = place_order(portfolio_id=1, ticker='AAPL', quantity=5)
    assert result == True
    updated_investment = db_session.query(Investment).filter_by(portfolio_id=1, Ticker='AAPL').first()
    assert updated_investment.Qty == 15

def test_place_order_no_existing_investment(db_session, monkeypatch):
    monkeypatch.setattr('app.services.security_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.login_services.current_user', 'testuser')
    
    user = User(username='testuser', password='password', firstname='First', lastname='Last', balance=10000)
    portfolio = Portfolio(id=1, name='Test Portfolio', description='Test Description', owner='testuser')
    security = Security(symbol='AAPL', issuer='Apple Inc.', name='Apple Stock', price=150.0)
   
    db_session.add(user)
    db_session.add(portfolio)
    db_session.add(security)
    db_session.commit()
    
    result = place_order(portfolio_id=1, ticker='AAPL', quantity=10)
   
    assert result == True
    
    new_investment = db_session.query(Investment).filter_by(portfolio_id=1, Ticker='AAPL').first()
   
    assert new_investment is not None
    assert new_investment.Qty == 10

def test_place_order_portfolio_not_owned(db_session, monkeypatch):
    monkeypatch.setattr('app.services.security_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.login_services.current_user', 'otheruser')
    
    user = User(username='testuser', password='password', firstname='First', lastname='Last', balance=10000)
    portfolio = Portfolio(id=1, name='Test Portfolio', description='Test Description', owner='testuser')
    security = Security(symbol='AAPL', issuer='Apple Inc.', name='Apple Stock', price=150.0)
    db_session.add(user)
    db_session.add(portfolio)
    db_session.add(security)
    db_session.commit()

    result = place_order(portfolio_id=1, ticker='AAPL', quantity=1)
    assert result is False

def test_place_order_no_current_user(db_session, monkeypatch):
    monkeypatch.setattr('app.services.security_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.login_services.current_user', None)
    
    security = Security(symbol='AAPL', issuer='Apple Inc.', name='Apple Stock', price=150.0)
    db_session.add(security)
    db_session.commit()

    result = place_order(portfolio_id=1, ticker='AAPL', quantity=1)
    assert result is False
