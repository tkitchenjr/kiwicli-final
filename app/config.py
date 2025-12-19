def database_config():
    return {
    'user': "root",
    'password': "Cheeseit22",
    'host': "localhost",
    'port': "3306",
    'db_name': "kiwidb"
    }

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{database_config().get('user')}:{database_config().get('password')}@{database_config().get('host')}:{database_config().get('port')}/{database_config().get('db_name')}"
