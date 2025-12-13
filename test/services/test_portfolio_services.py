import pytest
from app.domain.Portfolio import Portfolio
from app.domain.User import User
from app.domain.Investment import Investment
from app.domain.Security import Security
from app.services.portfolio_services import create_portfolio, delete_portfolio, view_all_portfolios, view_holdings, liquidate_portfolio

def test_create_portfolio_success(db_session, monkeypatch):
    monkeypatch.setattr('app.services.portfolio_services.get_session', lambda: db_session)
    
    result = create_portfolio('testuser', 'Test Portfolio', 'Test Description')
    
    assert result == True
    assert db_session.query(Portfolio).count() == 1
    assert db_session.query(Portfolio).first().name == "Test Portfolio"

def test_create_portfolio_missing_name(db_session, monkeypatch):
    monkeypatch.setattr('app.services.portfolio_services.get_session', lambda: db_session)

    result = create_portfolio('testuser', None, 'Desc')

    assert result is False
    assert db_session.query(Portfolio).count() == 0

def test_create_portfolio_missing_description(db_session, monkeypatch):
    monkeypatch.setattr('app.services.portfolio_services.get_session', lambda: db_session)

    result = create_portfolio('testuser', 'Name', None)

    assert result is False
    assert db_session.query(Portfolio).count() == 0

def test_delete_portfolio_success(db_session, monkeypatch):
    monkeypatch.setattr('app.services.portfolio_services.get_session', lambda: db_session)
    
    portfolio = Portfolio(id=1, name='Test Portfolio', description='Test Description', owner='testuser')
    db_session.add(portfolio)
    db_session.commit()
    
    result = delete_portfolio('testuser', 1)
    
    assert result is True
    assert db_session.query(Portfolio).count() == 0

def test_delete_portfolio_not_found(db_session, monkeypatch):
    monkeypatch.setattr('app.services.portfolio_services.get_session', lambda: db_session)
    
    result = delete_portfolio('testuser', 999)
    
    assert result is False
    assert db_session.query(Portfolio).count() == 0

def test_view_all_portfolios(db_session, monkeypatch):
    monkeypatch.setattr('app.services.portfolio_services.get_session', lambda: db_session)
    
    portfolio1 = Portfolio(id=1, name='Portfolio 1', description='Desc 1', owner='user1')
    portfolio2 = Portfolio(id=2, name='Portfolio 2', description='Desc 2', owner='user2')
    db_session.add(portfolio1)
    db_session.add(portfolio2)
    db_session.commit()
    
    result = view_all_portfolios()
    
    assert result is None
    assert db_session.query(Portfolio).count() == 2

def test_view_all_portfolios_no_portfolios(db_session, monkeypatch):
    monkeypatch.setattr('app.services.portfolio_services.get_session', lambda: db_session)
    
    result = view_all_portfolios()
    
    assert result is None
    assert db_session.query(Portfolio).count() == 0 

def test_view_holdings(db_session, monkeypatch):
    monkeypatch.setattr('app.services.portfolio_services.get_session', lambda: db_session)
    
    portfolio = Portfolio(id=1, name='Test Portfolio', description='Test Description', owner='testuser')
    security = Security(symbol='AAPL', name='Apple Inc', issuer='Apple', price=150.0)
    investment = Investment(portfolio_id=1, Ticker='AAPL', Qty=10, purchase_price=150.0)
    
    db_session.add(portfolio)
    db_session.add(security)
    db_session.add(investment)
    db_session.commit()
    
    result = view_holdings(1, 'testuser')
    
    assert result is None

def test_view_holdings_no_investments(db_session, monkeypatch):
    monkeypatch.setattr('app.services.portfolio_services.get_session', lambda: db_session)
    
    portfolio = Portfolio(id=1, name='Test Portfolio', description='Test Description', owner='testuser')
    db_session.add(portfolio)
    db_session.commit()
    
    result = view_holdings(1, 'testuser')
    
    assert result is None

def test_liquidate_portfolio_success(db_session, monkeypatch):
    monkeypatch.setattr('app.services.portfolio_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)
    inputs = iter(["1", "Y"])
    monkeypatch.setattr('app.services.portfolio_services._console.input', lambda prompt='': next(inputs))
    
    user = User(username='testuser', password='pw', firstname='First', lastname='Last', balance=0)
    portfolio = Portfolio(id=1, name='Test Portfolio', description='Test Description', owner='testuser')
    security = Security(symbol='AAPL', name='Apple Inc', issuer='Apple', price=150.0)
    investment = Investment(portfolio_id=1, Ticker='AAPL', Qty=10, purchase_price=150.0)
    
    db_session.add(user)
    db_session.add(portfolio)
    db_session.add(security)
    db_session.add(investment)
    db_session.commit()
    
    result = liquidate_portfolio('testuser')
    
    assert result is None

def test_liquidate_portfolio_not_found(db_session, monkeypatch):
    monkeypatch.setattr('app.services.portfolio_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.portfolio_services._console.input', lambda prompt='': "999")
    
    result = liquidate_portfolio('testuser')
    
    assert result is None

def test_liquidate_portfolio_no_investments(db_session, monkeypatch):
    monkeypatch.setattr('app.services.portfolio_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.transaction_services.get_session', lambda: db_session)
    monkeypatch.setattr('app.services.portfolio_services._console.input', lambda prompt='': "1")
    
    portfolio = Portfolio(id=1, name='Test Portfolio', description='Test Description', owner='testuser')
    db_session.add(portfolio)
    db_session.commit()
    
    result = liquidate_portfolio('testuser')
    
    assert result is None

def test_view_holdings_access_denied(db_session, monkeypatch):
    monkeypatch.setattr('app.services.portfolio_services.get_session', lambda: db_session)
    
    portfolio = Portfolio(id=1, name='Test Portfolio', description='Test Description', owner='owneruser')
    db_session.add(portfolio)
    db_session.commit()
    
    result = view_holdings(1, 'otheruser')
    
    assert result is None

def test_delete_portfolio_not_owner(db_session, monkeypatch):
    monkeypatch.setattr('app.services.portfolio_services.get_session', lambda: db_session)
    
    portfolio = Portfolio(id=1, name='Test Portfolio', description='Test Description', owner='someone_else')
    db_session.add(portfolio)
    db_session.commit()
    
    result = delete_portfolio('testuser', 1)
    
    assert result is False
    assert db_session.query(Portfolio).count() == 1
