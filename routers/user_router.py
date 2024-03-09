from flask import Blueprint, request, jsonify
from loguru import logger  # Importing Loguru logger
from helper.database_helper import DatabaseHelper
from utilities.validations import (
    validate_add_user_request,
    validate_get_user_logs_request,
)

# Creating a Blueprint for user routes
user_routes = Blueprint('user_routes', __name__)

# Creating an instance of the DatabaseHelper
db_helper = DatabaseHelper()

@user_routes.route('/add-user', methods=['POST'])
def add_user():
    """
    Endpoint for adding a user.

    Accepts a JSON payload containing a username.
    Validates the request, creates a user, and returns the user_id.
    """
    data = request.get_json()

    # Validate the add user request
    validation_result = validate_add_user_request(data)
    if validation_result:
        logger.error(f"Validation failed for add user request: {validation_result}")
        return jsonify(validation_result), 400

    # Extracting the username from the request data
    username = data.get('username')

    try:
        # Creating a new user in the database
        user_id = db_helper.create_user(username)

        logger.info(f"User '{username}' added with user_id: {user_id}")

        # Returning the user_id in the response
        return jsonify({"user_id": user_id})
    except Exception as e:
        logger.error(f"Error adding user '{username}': {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

@user_routes.route('/user-logs/<user_id>', methods=['GET'])
def get_user_logs(user_id):
    """
    Endpoint for retrieving logs for a specific user.

    Accepts a user_id parameter in the URL.
    Validates the request, retrieves and formats user logs, and returns them in ascending order of timestamp.
    """
    # Validate the get user logs request
    validation_result = validate_get_user_logs_request(user_id)
    if validation_result:
        logger.error(f"Validation failed for get user logs request: {validation_result}")
        return jsonify(validation_result), 400

    try:
        # Retrieving user logs from the database
        logs = db_helper.get_user_logs(user_id)

        # Transforming the logs into the desired format
        formatted_logs = [
            {
                "user": log[2],         # Prompt
                "assistant": log[3],    # Completion
                "time": log[4]           # Timestamp
            }
            for log in logs
        ]

        # Sorting the logs by timestamp in ascending order
        sorted_logs = sorted(formatted_logs, key=lambda x: x["time"])

        logger.info(f"User logs retrieved for user_id {user_id}")

        # Returning the logs in the response
        return jsonify({"logs": sorted_logs})
    except Exception as e:
        logger.error(f"Error retrieving user logs for user_id {user_id}: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
