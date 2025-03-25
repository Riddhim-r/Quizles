from dotenv import load_dotenv 
import os 
load_dotenv() # load the .env file in the root directory

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///database.db')
    # get the DATABASE_URL from the .env file and from load.enf store it in the app.config['SQLALCHEMY_DATABASE_URI']

    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
