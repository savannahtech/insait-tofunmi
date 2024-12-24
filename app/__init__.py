
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_openapi3 import OpenAPI
from flask_swagger_ui import get_swaggerui_blueprint
import os
from flask import Flask, jsonify
from werkzeug.exceptions import MethodNotAllowed
import logging


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, static_url_path='/static')

    app.config.from_object("app.config.Config")
    
    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import question_blueprint as routes_bp
    app.register_blueprint(routes_bp)

    # SWAGGER_URL = '/'
    SWAGGER_URL = '/api/docs'  # URL for the Swagger UI

    API_URL = '/static/swagger.json'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Test Application"
        },
    )
    app.register_blueprint(swaggerui_blueprint)
    app.config['DEBUG'] = True
    app.config['ENV'] = 'development'

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({
            'error': 'Method not allowed',
            'message': 'The method is not allowed for this endpoint'
        }), 405
    
    return app


# Create application instance
application = create_app()
app = application

# If you want to run the app directly
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(
        
        host='0.0.0.0',
        port=5000,
        debug=True 
    )

