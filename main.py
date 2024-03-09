from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from loguru import logger  
from routers.openai_router import ai_routes
from routers.user_router import user_routes

app = Flask(__name__)
app.register_blueprint(ai_routes, url_prefix='/ai_services')
app.register_blueprint(user_routes, url_prefix='/users')

# Initialize Flask-Limiter
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["5 per minute"]  # Adjust the rate limit based on your needs
)

if __name__ == "__main__":
    try:
        logger.info("Starting the application.")
        app.run(debug=True)
    except Exception as e:
        logger.error(f"Error starting the application: {str(e)}")
