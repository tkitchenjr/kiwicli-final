import pytest
from app.domain.User import User
from app.services.user_services import add_user, delete_user, view_users, list_users
from app.domain.Portfolio import Portfolio


def test_add_user(db_session, monkeypatch):
    monkeypatch.setattr('app.services.user_services.get_session', lambda: db_session)

    result = add_user(username='testuser', password='password', firstname='First', lastname='Last', balance=5000)

    assert result == True
    assert db_session.query(User).count() == 1
    assert db_session.query(User).first().username == "testuser"
   
def test_add_user_duplicate_username(db_session, monkeypatch):
    monkeypatch.setattr('app.services.user_services.get_session', lambda: db_session)

    existing_user = User(username='testuser', password='password', firstname='First', lastname='Last', balance=5000)
    db_session.add(existing_user)
    db_session.commit()

    result = add_user(username='testuser', password='password2', firstname='Second', lastname='User', balance=3000)

    assert result == False
    assert db_session.query(User).count() == 1

def test_add_user_empty_lastname(db_session, monkeypatch):
    monkeypatch.setattr('app.services.user_services.get_session', lambda: db_session)

    result = add_user(username='testuser', password='password', firstname='First', lastname='', balance=100)

    assert result == True 
    assert db_session.query(User).count() == 1 

def test_add_user_negative_balance(db_session, monkeypatch):
    monkeypatch.setattr('app.services.user_services.get_session', lambda: db_session)

    result = add_user(username='testuser', password='password', firstname='First', lastname='Last', balance=-100)

    assert result == True
    assert db_session.query(User).count() == 1
    assert db_session.query(User).first().balance == -100

def test_add_user_zero_balance(db_session, monkeypatch):
    monkeypatch.setattr('app.services.user_services.get_session', lambda: db_session)

    result = add_user(username='testuser', password='password', firstname='First', lastname='Last', balance=0)

    assert result == True
    assert db_session.query(User).count() == 1
    assert db_session.query(User).first().balance == 0

def test_delete_user_success(db_session, monkeypatch):
    monkeypatch.setattr('app.services.user_services.get_session', lambda: db_session)

    user = User(username='testuser', password='password', firstname='First', lastname='Last', balance=100)
    db_session.add(user)
    db_session.commit()

    result = delete_user(username='testuser')

    assert result == True
    assert db_session.query(User).count() == 0

def test_delete_user_not_found(db_session, monkeypatch):
    monkeypatch.setattr('app.services.user_services.get_session', lambda: db_session)

    result = delete_user(username='nonexistent')

    assert result == False
    assert db_session.query(User).count() == 0

def test_delete_admin_protection(db_session, monkeypatch):
    monkeypatch.setattr('app.services.user_services.get_session', lambda: db_session)

    admin = User(username='admin', password='password', firstname='Admin', lastname='User', balance=0)
    db_session.add(admin)
    db_session.commit()

    result = delete_user(username='admin')

    assert result == False
    assert db_session.query(User).count() == 1

def test_delete_user_empty_username(db_session, monkeypatch):
    monkeypatch.setattr('app.services.user_services.get_session', lambda: db_session)

    user = User(username='', password='password', firstname='First', lastname='Last', balance=100)
    db_session.add(user)
    db_session.commit()

    result = delete_user(username=' ')
    
    assert result == False
    assert db_session.query(User).count() == 1

def test_delete_user_with_portfolio(db_session, monkeypatch):
    monkeypatch.setattr('app.services.user_services.get_session', lambda: db_session)

    user = User(username ='user1', password='password', firstname='first', lastname='last', balance = 1000)
    db_session.add(user)
    db_session.commit()

    portfolio = Portfolio(id='1', owner='user1', name='Test Portfolio')
    db_session.add(portfolio)
    db_session.commit()

    monkeypatch.setattr('app.services.user_services._console.input', lambda prompt: '')
    
    result = delete_user(username='user1')
    assert result == False
    assert db_session.query(User).count() == 1

def test_view_users(db_session,monkeypatch):
    monkeypatch.setattr('app.services.user_services.get_session', lambda: db_session)

    user = User(username ='user1', password='password', firstname='first', lastname='last', balance = 1000)
    db_session.add(user)
    db_session.commit()

    result = view_users([user])
    assert result is None

def test_view_users_no_users(db_session, monkeypatch):
    monkeypatch.setattr('app.services.user_services.get_session', lambda: db_session)
    
    result = view_users([])
    assert result is None

def test_list_users(db_session, monkeypatch):
    monkeypatch.setattr('app.services.user_services.get_session', lambda: db_session)

    user1 = User(username ='user1', password='password', firstname='first', lastname='last', balance = 1000)
    user2 = User(username ='user2', password='password', firstname='first2', lastname='last2', balance = 2000)
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()

    users = list_users()
    assert len(users) == 2
    assert users[0].username == 'user1'
    assert users[1].username == 'user2'

def test_list_users_no_users(db_session, monkeypatch):
    monkeypatch.setattr('app.services.user_services.get_session', lambda: db_session)

    result = list_users()

    users = list_users()
    assert len(users) == 0
    assert result == []



