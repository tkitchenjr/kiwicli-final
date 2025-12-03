def database_config():
    user = "tkitchenjr"
    password = "Cheeseit22"
    host = "localhost"
    port = "3306"
    db_name = "kiwidb"
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

