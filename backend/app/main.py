import os
from flask import Flask, jsonify
from app.config import ProductionConfig, DevelopmentConfig
from app.controllers import user_bp, role_bp, permissions_bp, site_bp, search_results_bp, user_sites_bp, site_stats_bp

app = Flask(__name__)

# App exception handling
@app.errorhandler(Exception)
def handle_error(error):
    response = {
        'message': 'An unexpected error has occurred on the server.',
        'error': str(error)
    }
    return jsonify(response), 500

# import controllers and regristation them.
app.register_blueprint(user_bp)
app.register_blueprint(role_bp)
app.register_blueprint(permissions_bp)
app.register_blueprint(site_bp)
app.register_blueprint(search_results_bp)
app.register_blueprint(user_sites_bp)
app.register_blueprint(site_stats_bp)   
    

# Runtime environment validation and run application.
def run_app():
    config = os.environ.get('FLASK_ENV', 'production')
    if config == 'development':
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)



if __name__ == '__main__':
    run_app()
