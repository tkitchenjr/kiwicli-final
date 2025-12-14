import pytest
from app.domain.User import User
from app.services.login_services import get_login_inputs, login

def test_get_login_inputs(monkeypatch):
    inputs = iter(["testuser", "password123"])
    monkeypatch.setattr('app.services.login_services._console.input', lambda prompt='': next(inputs))

    username, password = get_login_inputs()

    assert username == "testuser"
    assert password == "password123"

def test_login_success(db_session, monkeypatch):
    monkeypatch.setattr('app.services.login_services.get_session', lambda: db_session)

    user = User(username='testuser', password='password123', firstname='Test', lastname='User', balance=100)
    db_session.add(user)
    db_session.commit()

    result = login(username='testuser', password='password123')

    assert result is True

def test_login_incorrect_username(db_session, monkeypatch):
    monkeypatch.setattr('app.services.login_services.get_session', lambda: db_session)

    user = User(username='testuser', password='password123', firstname='Test', lastname='User', balance=100)
    db_session.add(user)
    db_session.commit()

    result = login(username='wronguser', password='password123')

    assert result is False

def test_login_incorrect_password(db_session, monkeypatch):
    monkeypatch.setattr('app.services.login_services.get_session', lambda: db_session)

    user = User(username='testuser', password='password123', firstname='Test', lastname='User', balance=100)
    db_session.add(user)
    db_session.commit()

    result = login(username='testuser', password='wrongpassword')

    assert result is False
