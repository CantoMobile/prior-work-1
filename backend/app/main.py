import os
from flask import Flask, jsonify
from flask_cors import CORS
from app.config import ProductionConfig, DevelopmentConfig
from app.controllers import (
    user_bp,
    role_bp,
    permissions_bp,
    site_bp,
    search_results_bp,
    user_sites_bp,
    site_stats_bp,
    reviews_bp,
    admin_bp,
    category_bp,
    recommendations_bp,
    referrals_bp,
    points_system_bp,
    user_actions_bp
)
from app.utils.logger import logger
from app.models.user_model import User
from app.models.site_model import Site

app = Flask(__name__)

#Allow cors 
cors = CORS(app, resources={r'*': {'origins': '*'}})
app.config['CORS_HEADERS'] = 'Content-Type, Authorization'

# App exception handling
@app.errorhandler(Exception)
def handle_error(error):
    response = {
        'message': 'An unexpected error has occurred on the server.',
        'error': str(error)
    }
    logger.error(response)
    return jsonify(response), 500


# import controllers and regristation them.
app.register_blueprint(user_bp)
app.register_blueprint(role_bp)
app.register_blueprint(permissions_bp)
app.register_blueprint(site_bp)
app.register_blueprint(search_results_bp)
app.register_blueprint(user_sites_bp)
app.register_blueprint(site_stats_bp) 
app.register_blueprint(category_bp)   
app.register_blueprint(recommendations_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(admin_bp)  
app.register_blueprint(referrals_bp) 
app.register_blueprint(points_system_bp)
app.register_blueprint(user_actions_bp)


# Runtime environment validation and run application.
def run_app():
    config = os.environ.get('FLASK_ENV', 'production')
    if config == 'development':
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)



if __name__ == '__main__':
    run_app()
