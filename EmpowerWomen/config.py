class Config:
    SECRET_KEY = 'cxk-666'

    # 数据库配置
    DB_USER = 'TP01Master'
    DB_PASSWORD = 'Pass!TP01'
    DB_HOST = 'fit5120harmonyseekers.cz2s4m6aa5w7.ap-southeast-2.rds.amazonaws.com'
    DB_PORT = '3306'
    DB_NAME = 'TP01'

    # 构建SQLAlchemy的数据库URI
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
