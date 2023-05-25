import json
import os
import click
from flask import Flask, jsonify, g
from config import ProductionConfig, DevelopmentConfig
from config import database as dbase


app = Flask(__name__)

# Instance database
db = dbase.connect()

# App exception handling


@app.errorhandler(Exception)
def handle_error(error):
    response = {
        'message': 'An unexpected error has occurred on the server.',
        'error': str(error)
    }
    return jsonify(response), 500


# Runtime environment validation and run application.
@click.command()
@click.option('--config', default='development', help='Configuration (development or production)')
def run_app(config):
    os.environ['FLASK_ENV'] = config
    if config == 'production':
        app.config.from_object(ProductionConfig)
    elif config == 'development':
        app.config.from_object(DevelopmentConfig)

    app.config['MONGO_URI'] = app.config['MONGO_URI']
    app.run()


if __name__ == '__main__':
    from controllers import user_bp, auth_bp, role_bp, permissions_bp, site_bp, search_results_bp, user_sites_bp, site_stats_bp
    # import controllers and regristation them.
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(permissions_bp)
    app.register_blueprint(site_bp)
    app.register_blueprint(search_results_bp)
    app.register_blueprint(user_sites_bp)
    app.register_blueprint(site_stats_bp)
    run_app()
