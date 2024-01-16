from flask import Flask
from flask_cors import CORS

from .extension import db
from .routes import app

def create_app():
    main = Flask(__name__)
    main.json.ensure_ascii = False

    # Cho phép tất cả các nguồn
    CORS(main)

    main.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://detect_jewelry_user:XbkT1JiGnhAHJCAmcotTN40FBHwWuFX3@dpg-cmbbvrmd3nmc73eptejg-a.oregon-postgres.render.com/detect_jewelry"
    db.init_app(main)

    main.register_blueprint(app)

    return main