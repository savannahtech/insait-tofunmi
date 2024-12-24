# app/errors/handlers.py
from flask import Blueprint, jsonify
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from openai import OpenAIError
from app.schemas import ErrorResponse
import logging

error_blueprint = Blueprint('errors', __name__)

class APIError(Exception):
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_response(self):
        return ErrorResponse(
            error=self.message,
            details=self.payload,
            status_code=self.status_code
        ).dict()

@error_blueprint.app_errorhandler(ValidationError)
def handle_validation_error(error):
    logging.error(f"Validation error: {error.json()}")
    response = ErrorResponse(
        error="Validation error",
        details=error.errors(),
        status_code=422
    )
    return jsonify(response.dict()), 422

@error_blueprint.app_errorhandler(SQLAlchemyError)
def handle_db_error(error):
    logging.error(f"Database error: {str(error)}")
    response = ErrorResponse(
        error="Database error occurred",
        status_code=500
    )
    return jsonify(response.dict()), 500

@error_blueprint.app_errorhandler(OpenAIError)
def handle_openai_error(error):
    logging.error(f"OpenAI API error: {str(error)}")
    response = ErrorResponse(
        error="AI Service error",
        status_code=503
    )
    return jsonify(response.dict()), 503

@error_blueprint.app_errorhandler(APIError)
def handle_api_error(error):
    logging.error(f"API error: {error.message}")
    response = error.to_response()
    return jsonify(response), error.status_code

@error_blueprint.app_errorhandler(Exception)
def handle_generic_error(error):
    logging.error(f"Unexpected error: {str(error)}")
    response = ErrorResponse(
        error="Internal server error",
        status_code=500
    )
    return jsonify(response.dict()), 500