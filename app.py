import logging
import os
from flask import Flask, request, jsonify
from main import chain  # Assuming you have a 'chain' object in 'main.py'

# Initialize Flask app
app = Flask(__name__)

# Configure Flask app with environment variables (production, development, etc.)
app.config.from_mapping(
    ENV=os.getenv('FLASK_ENV', 'development'),  # Automatically pull environment from system env variables
    DEBUG=os.getenv('FLASK_DEBUG', 'True') == 'True',  # Convert string to boolean
    SECRET_KEY=os.getenv('SECRET_KEY', 'your_secret_key'),  # Use environment variable or default
    LOGGING_LEVEL=os.getenv('LOGGING_LEVEL', 'DEBUG').upper()  # Default to 'DEBUG'
)
from flask_cors import CORS

# Enable CORS
CORS(app)

# Set up logging
logging.basicConfig(
    level=app.config['LOGGING_LEVEL'],
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Example to demonstrate logging at various levels
logger.debug("Logging initialized")

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Ensure the request contains JSON data
        if not request.is_json:
            logger.error('Request must be in JSON format')
            return jsonify({'error': 'Request must be in JSON format'}), 400
        
        # Get the user input from the request body
        user_message = request.json.get('message', None)
        
        # Check if message is provided
        if not user_message:
            logger.warning('No message provided in the request')
            return jsonify({'error': 'No message provided!'}), 400
        
        # Optional: Add more data/context (like user services or session data)
        services = "Service information or relevant context"

        # Invoke the AI chain to process the user message
        logger.info(f"User message: {user_message}")
        result = chain.invoke({"services": services, "question": user_message})

        # Return the response
        return jsonify({'answer': result}), 200

    except ValueError as ve:
        # Handle specific exceptions like value errors
        logger.error(f"Value error occurred: {str(ve)}")
        return jsonify({'error': 'Invalid value provided.'}), 400
    except KeyError as ke:
        # Handle specific exceptions like missing key errors
        logger.error(f"Missing key: {str(ke)}")
        return jsonify({'error': 'Missing expected data.'}), 400
    except Exception as e:
        # Catch all other exceptions
        logger.error(f"Unexpected error occurred: {str(e)}")
        return jsonify({'error': f'Error: {str(e)}'}), 500


# Health check route for monitoring
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200


# Run the Flask app only if executed directly
if __name__ == '__main__':
    # Load host and port from environment variables, defaulting to '0.0.0.0' and port 5000
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))

    app.run(host=host, port=port, debug=app.config['DEBUG'], use_reloader=False)  # Avoid reloader on Windows
