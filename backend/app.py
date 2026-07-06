from flask import Flask
from flask_cors import CORS
from routes.register_API import register_bp
from routes.user_login_API import login_bp
from routes.ask_AI_API import AI_bp
from routes.chat_API import chat_bp
from routes.member_API import member_bp
from routes.password_reset_API import password_reset_bp

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

# Register Blueprints
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(AI_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(member_bp)
app.register_blueprint(password_reset_bp )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)