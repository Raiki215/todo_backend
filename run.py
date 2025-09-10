from app import create_app
from flask_login import login_user, logout_user, login_required, current_user
# test用
from app import get_todos
get_todos.getAll_todos(2)

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)