from flask import Flask 
from dotenv import load_dotenv 
import os

def configure():
    load_dotenv()

def create_app():
    configure()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "os.getenv('secret_key')"

    from .views import views 
    from .calc import calc

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(calc, url_prefix="/")

    return app 


