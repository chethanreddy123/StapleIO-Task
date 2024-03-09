from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from loguru import logger 

from helper.open_ai_completion import OpenAICompletionService
from helper.database_helper import DatabaseHelper
from utilities.validations import validate_openai_completion_request

# Creating a Blueprint for AI services
ai_routes = Blueprint('ai_services', __name__)

# Creating instances of services and helpers
openai_service = OpenAICompletionService()
db_helper = DatabaseHelper()

# Route for OpenAI completion service
@ai_routes.route('/openai-completion', methods=['POST'])
def openai_completion():
    """
    Endpoint for OpenAI completion service.
    
    Accepts a JSON payload containing user_id and prompt.
    Retrieves completion from OpenAI service, logs it to the database, and returns the completion.
    """
    data = request.get_json()

    # Validate the OpenAI completion request
    validation_result = validate_openai_completion_request(data)
    if validation_result:
        logger.error(f"Validation failed: {validation_result}")
        return jsonify(validation_result), 400

    # Extracting user_id and prompt from the request data
    user_id = data.get('user_id')
    prompt = data.get('prompt')

    try:
        # Getting completion from OpenAI service
        completion = openai_service.get_completion(user_id, prompt)

        # Logging completion to the database
        db_helper.log_to_database(user_id, prompt, completion)
        
        logger.info(f"Completion logged for user {user_id}: {completion}")

        # Returning the completion in the response
        return jsonify({"completion": completion})
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
