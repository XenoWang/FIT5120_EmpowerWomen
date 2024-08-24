class Config:
    SECRET_KEY = 'cxk-666'
    DB_USER = 'TP01Master'
    DB_PASSWORD = 'Pass!TP01'
    DB_HOST = 'fit5120harmonyseekers.cz2s4m6aa5w7.ap-southeast-2.rds.amazonaws.com'
    DB_PORT = '3306'
    DB_NAME = 'TP01'

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
