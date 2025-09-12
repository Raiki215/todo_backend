from app import create_app
from flask_login import login_user, logout_user, login_required, current_user
import os


app = create_app()
app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config['SESSION_COOKIE_SECURE'] = True

if __name__ == "__main__":
    app.run(debug=True)