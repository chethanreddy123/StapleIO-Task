# helper/open_ai_completion.py
import os
import openai
from loguru import logger  # Importing Loguru logger
from helper.database_helper import DatabaseHelper

class OpenAICompletionService:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.db_helper = DatabaseHelper()

    def get_completion(self, user_id, prompt):
        """
        Get completion for a user prompt using OpenAI Chat API.

        :param user_id: User identifier
        :param prompt: User prompt
        :return: OpenAI completion response
        """
        try:
            return self._get_single_completion(user_id, prompt)
        except Exception as e:
            logger.error(f"Error getting completion for user {user_id}: {str(e)}")
            return None

    def _get_single_completion(self, user_id, prompt):
        """
        Get a single completion using OpenAI Chat API.

        :param user_id: User identifier
        :param prompt: User prompt
        :return: OpenAI completion response
        """
        try:
            # Fetch user messages from the database
            user_messages = self.db_helper.get_user_logs(user_id)

            # Prepare messages for OpenAI completion
            messages = [{"role": "system", "content": "You are a helpful assistant. Make sure that answers are clear and concise."}]
            for message in user_messages:
                messages.append({"role": "user", "content": message[2]})
                messages.append({"role": "assistant", "content": message[3]})
            messages.append({"role": "user", "content": prompt})

            # Call OpenAI completion
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            completion = response.choices[0].message.content
            return completion
        except Exception as e:
            logger.error(f"Error getting single completion for user {user_id}: {str(e)}")
            return None

    def log_to_database(self, user_id, prompt, completion):
        """
        Log user interaction to the database.

        :param user_id: User identifier
        :param prompt: User prompt
        :param completion: OpenAI completion
        """
        try:
            self.db_helper.log_to_database(user_id, prompt, completion)
            logger.info(f"Interaction logged for user {user_id}")
        except Exception as e:
            logger.error(f"Error logging interaction for user {user_id}: {str(e)}")

    def get_logs(self):
        """
        Get all logs from the database.

        :return: List of logs
        """
        try:
            return self.db_helper.get_logs()
        except Exception as e:
            logger.error(f"Error getting logs: {str(e)}")
            return None