class Config:

    # 数据库配置
    DB_USER = 'TP01Master'
    DB_PASSWORD = 'Pass!TP01'
    DB_HOST = 'fit5120harmonyseekers.cz2s4m6aa5w7.ap-southeast-2.rds.amazonaws.com'
    DB_PORT = '3306'
    DB_NAME = 'TP01'

    # 构建SQLAlchemy的数据库URI
    DB_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_DATABASE_URI = DB_URI

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
