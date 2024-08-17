class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://main:password@127.0.0.1/food_manager_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key'