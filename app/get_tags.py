from flask_login import current_user
from .db_connection import get_connection
from flask import jsonify

def getAll_tags():
    user_id = current_user.user_id
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # ユーザーに関連するタグを取得するクエリ
        # ユーザーのTodoに関連付けられたタグを取得
        sql = """
        SELECT DISTINCT t.tag_id, t.tag 
        FROM tags t
        INNER JOIN todo_to_tag tt ON t.tag_id = tt.tag_id
        INNER JOIN todos td ON tt.todo_id = td.todo_id
        WHERE td.user_id = %s AND tt.delete_flg = FALSE AND td.delete_flg = FALSE
        ORDER BY t.tag
        """

        cursor.execute(sql, (user_id,))
        tags = [{"tag_id": tag[0], "tag": tag[1]} for tag in cursor.fetchall()]

        return jsonify({"success": True, "tags": tags}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()