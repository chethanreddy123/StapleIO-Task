from helper.database_helper import DatabaseHelper
from loguru import logger  # Importing Loguru logger

db_helper = DatabaseHelper()

def validate_openai_completion_request(data):
    """
    Validate the request data for OpenAI completion.

    :param data: Request data
    :return: None if validation passes, error message otherwise
    """
    try:
        # Check if 'user_id' and 'prompt' are present in the request data
        if 'user_id' not in data or 'prompt' not in data:
            return {"error": "'user_id' and 'prompt' are required fields"}

        user_id = data['user_id']
        prompt = data['prompt']

        # Check if 'prompt' is not more than 1000 characters
        if len(prompt) > 1000:
            return {"error": "Prompt exceeds the maximum allowed length (1000 characters)"}

        # Check if 'user_id' is valid (exists in the database)
        if not db_helper.is_valid_user(user_id):
            return {"error": "Invalid user_id"}

        # All validations passed
        return None
    except Exception as e:
        logger.error(f"Error validating OpenAI completion request: {str(e)}")
        return {"error": "Internal Server Error"}


def validate_add_user_request(data):
    """
    Validate the request data for adding a user.

    :param data: Request data
    :return: None if validation passes, error message otherwise
    """
    try:
        # Check if 'username' is present in the request data
        if 'username' not in data:
            return {"error": "Missing 'username' in request data"}

        username = data['username']

        # Check if 'username' is not empty
        if not username:
            return {"error": "Username cannot be empty"}

        # Check if the username already exists in the database
        if db_helper.is_valid_user(username):
            return {"error": "Username already exists"}

        # You can add additional validations for 'username' length, format, etc. if needed

        # All validations passed
        return None
    except Exception as e:
        logger.error(f"Error validating add user request: {str(e)}")
        return {"error": "Internal Server Error"}


def validate_get_user_logs_request(user_id):
    """
    Validate the request data for getting user logs.

    :param user_id: User identifier
    :return: None if validation passes, error message otherwise
    """
    try:
        # Check if 'user_id' is a valid integer
        if user_id == "":
            return {"error": "user_id cannot be empty"}

        # Check if the user with the given user_id exists in the database
        if not db_helper.is_valid_user(user_id):
            return {"error": f"User with user_id {user_id} not found"}

        # All validations passed
        return None
    except Exception as e:
        logger.error(f"Error validating get user logs request: {str(e)}")
        return {"error": "Internal Server Error"}
