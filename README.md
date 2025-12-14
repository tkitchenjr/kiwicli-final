1. Create Virtual Environment
2. install dependencies in requirements.txt into virtual environment
3. Ensure Root folder is at kiwicli package 

4. Testing
For Unit Testing run pytest -q to run from root repository
For Code coverage run pytest --cov=app

5. For Codespace CLI APP operation run python -m app.main
   - Database URL is taken from the DATABASE_URL env var.
   - If DATABASE_URL is not set, the app auto-creates and uses a local SQLite file at ./kiwidb.sqlite.
   - Tables are bootstrapped automatically on first session use.

Credentials to Log in as admin
username: admin
password: admin


## Database configuration

- Configuration lives in app/config.py and should return a database URL string via database_config().
- To point at your own DB: export DATABASE_URL="mysql+pymysql://user:pw@host:3306/kiwidb" (or any SQLAlchemy URL).
- For a quick local run with no setup, do nothing; it will default to SQLite at ./kiwidb.sqlite.
- On the first call to get_session(), the app runs Base.metadata.create_all(engine) to create missing tables in the configured DB.
