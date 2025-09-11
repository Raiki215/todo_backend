from flask import jsonify, request
from flask_login import current_user
import json
from .db_connection import get_connection

def get_notification_history():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        user_id = current_user.user_id
        cursor.execute("""
        SELECT n.notification_id,
            n.message,
            n.read_flg,
            t.todo_id,
            t.todo,
            t.deadline
        FROM
            notifications n
        JOIN
            todos t ON n.todo_id = t.todo_id
        WHERE
            n.user_id = %s AND n.delete_flg = FALSE
        ORDER BY
            n.created_at DESC""", (user_id,))
        conn.commit()
        notifications = cursor.fetchall()
        columns = []
        for desc in cursor.description:
            columns.append(desc[0])
        result = []
        for row in notifications:
            item = {}
            for col, val in zip(columns, row):
                item[col] = val
            result.append(item)
        return jsonify(result), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()

def insert_notification(todo_id, user_id, message):
    conn = get_connection()
    try:
        sql = """
        INSERT INTO notifications (todo_id, user_id, message) VALUES (%s, %s, %s)
        """
        cursor = conn.cursor()
        cursor.execute(sql, (todo_id, user_id, message))

        conn.commit()
        notification = cursor.fetchone()
        conn.commit()
        columns = [desc[0] for desc in cursor.description]
        result = dict(zip(columns, notification))
        return result, 201
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()
