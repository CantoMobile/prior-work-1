import logging
from functools import wraps
from flask import jsonify

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class CustomException(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

# Custom error codes
ERROR_CODE_INVALID_DATA = 1001
ERROR_CODE_DATABASE_ERROR = 1002

def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except CustomException as e:
            logger.error(f"Custom Exception: {str(e)}")
            return handle_custom_exception(e)
        except Exception as e:
            logger.exception("Unhandled Exception")
            return handle_unhandled_exception(e)
    return wrapper

def handle_custom_exception(error):
    error_response = {
        "error_code": error.error_code,
        "message": str(error),
        "details": None  # Include additional details if needed
    }
    # Return the formatted error response to the client
    return jsonify(error_response), 400

def handle_unhandled_exception(error):
    error_response = {
        "error_code": 5000,  # A generic error code for unhandled exceptions
        "message": "Internal Server Error",
        "details": None  # Include additional details if needed
    }
    # Return the formatted error response to the client
    return jsonify(error_response), 500
