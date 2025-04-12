from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    CORS(app)

    from app.routes.weather import weather_bp
    app.register_blueprint(weather_bp, url_prefix='/api')

    from app.routes.dbtest import dbtest_bp
    app.register_blueprint(dbtest_bp)

    from app.routes.gcs_upload import gcs_upload_bp
    app.register_blueprint(gcs_upload_bp)



    return app
