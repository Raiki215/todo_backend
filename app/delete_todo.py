from .db_connection import get_connection
from flask import request, jsonify, session
from flask_login import current_user
def del_Todo():
    data = request.json
    todo_id = int(data.get("todo_id"))
    user_id = current_user.user_id
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("update todos set delete_flg = TRUE where todo_id = %s",
                       (todo_id,))
        connection.commit()
        
        cursor.execute("update todo_to_tag set delete_flg = TRUE where todo_id = %s",
                       (todo_id,))
        connection.commit()

        cursor.execute("""
            SELECT DISTINCT t.tag_id, t.tag
            FROM tags t
            INNER JOIN todo_to_tag tt ON t.tag_id = tt.tag_id
            INNER JOIN todos td ON tt.todo_id = td.todo_id
            WHERE td.user_id = %s AND tt.delete_flg = FALSE AND td.delete_flg = FALSE
            ORDER BY t.tag
        """, (user_id,))
        all_tags = [{"tag_id": tag[0], "tag": tag[1]} for tag in cursor.fetchall()]
        
        return jsonify({
            "message": "削除が完了しました。",
            "todo_id": todo_id,
            "data" : data,
            "all_tags": all_tags
        }), 201
    except Exception as e:
        return jsonify({
            "error" : "error"
        }), 500
    finally:
        cursor.close()
        connection.close()
        
        
        
# def del_Tag():