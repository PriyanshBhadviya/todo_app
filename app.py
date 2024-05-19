from flask import Flask
from config import Config
from models import db
from schemas import ma
from views import task_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(task_bp, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

