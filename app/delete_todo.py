from .db_connection import get_connection
from flask import request, jsonify, session
from flask_login import current_user
def del_Todo():
    data = request.json
    todo_id = data.get("todo_id")
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("update todos set delete_flg = TRUE where todo_id = %s",
                       (todo_id,))
        connection.commit()
        
        cursor.execute("update todo_to_tag set delete_flg = TRUE where todo_id = %s",
                       (todo_id,))
        connection.commit()
        
        return jsonify({
            "message": "削除が完了しました。",
            "todo_id": todo_id,
            "data" : data
        }), 201
    except Exception as e:
        return jsonify({
            "error" : "error"
        }), 500
    finally:
        cursor.close()
        connection.close()
        
        
        
# def del_Tag():