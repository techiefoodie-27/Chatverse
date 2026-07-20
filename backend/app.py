from flask import Flask
from dotenv import load_dotenv

load_dotenv()
from config import Config

from extensions import db, login_manager

# Models
from models.user import User
from models.otp import OTPVerification

# Routes
from routes.auth import auth
from routes.otp import otp


# Create Flask app FIRST
app = Flask(__name__)

app.config.from_object(Config)


# Initialize extensions
db.init_app(app)

login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Register routes AFTER app exists
app.register_blueprint(auth, url_prefix="/api")
app.register_blueprint(otp, url_prefix="/api")


@app.route("/")
def home():
    return "Welcome to ChatVerse Database Connected!"


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)