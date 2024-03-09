import sqlite3
from datetime import datetime
from loguru import logger  # Importing Loguru logger

class DatabaseHelper:
    def __init__(self, db_path='log.sqlite'):
        self.db_path = db_path
        self.create_tables()

    def create_tables(self):
        """
        Create database tables if they don't exist.
        """
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    created_at TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    prompt TEXT,
                    completion TEXT,
                    timestamp TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')

            connection.commit()
            logger.info("Database tables created.")
        except Exception as e:
            logger.error(f"Error creating tables: {str(e)}")
        finally:
            connection.close()

    def create_user(self, username):
        """
        Create a new user and return the user_id.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            cursor.execute('INSERT INTO users (username, created_at) VALUES (?, ?)',
                           (username, timestamp))

            user_id = cursor.lastrowid
            connection.commit()
            logger.info(f"User '{username}' created with user_id: {user_id}")
            return user_id
        except Exception as e:
            logger.error(f"Error creating user '{username}': {str(e)}")
        finally:
            connection.close()

    def log_to_database(self, user_id, prompt, completion):
        """
        Log user interaction to the database.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            cursor.execute('INSERT INTO logs (user_id, prompt, completion, timestamp) VALUES (?, ?, ?, ?)',
                           (user_id, prompt, completion, timestamp))

            connection.commit()
            logger.info(f"Interaction logged for user_id {user_id}")
        except Exception as e:
            logger.error(f"Error logging interaction for user_id {user_id}: {str(e)}")
        finally:
            connection.close()

    def get_user_logs(self, user_id):
        """
        Retrieve logs for a specific user.
        """
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            cursor.execute('SELECT * FROM logs WHERE user_id = ?', (user_id,))
            logs = cursor.fetchall()
            return logs
        except Exception as e:
            logger.error(f"Error retrieving logs for user_id {user_id}: {str(e)}")
        finally:
            connection.close()

    def is_valid_user(self, user_id):
        """
        Check if a user with the given user_id exists in the database.
        """
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            cursor.execute('SELECT id FROM users WHERE username = ?', (user_id,))
            user_exists = cursor.fetchone() is not None
            return user_exists
        except Exception as e:
            logger.error(f"Error checking user existence for user_id {user_id}: {str(e)}")
        finally:
            connection.close()
