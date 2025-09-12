from flask import jsonify
from flask_login import current_user, login_required

@login_required
def get_current_user():
    """現在ログインしているユーザーの情報を取得"""
    try:
        user_data = {
            'user_id': current_user.user_id,
            'name': current_user.name,
            'email': current_user.email
        }
        return jsonify({
            'success': True,
            'user': user_data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500