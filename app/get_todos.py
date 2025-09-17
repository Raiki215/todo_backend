from flask_login import current_user
from .db_connection import get_connection
from flask import jsonify, request


def getAll_todos():
    user_id = current_user.user_id
    # user_id = 1
    connection = get_connection()
    try:
        cursor = connection.cursor()
        sql = """
            SELECT t.todo_id, t.todo, t.deadline, t.priority, t.finish_flg, t.estimated_time, t.pressure_flg, t.user_id,
                   tg.tag
            FROM todos t
            LEFT JOIN todo_to_tag tt ON t.todo_id = tt.todo_id AND tt.delete_flg = FALSE
            LEFT JOIN tags tg ON tt.tag_id = tg.tag_id
            WHERE t.user_id = %s AND t.delete_flg = FALSE
            ORDER BY t.priority DESC, t.todo_id ASC
        """
        cursor.execute(sql, (user_id,))
        result = cursor.fetchall()

        todos_dict = {}
        for row in result:
            todo_id = row[0]
            if todo_id not in todos_dict:
                todos_dict[todo_id] = {
                    "todo_id": row[0],
                    "todo": row[1],
                    "deadline": row[2],
                    "priority": row[3],
                    "finish_flg": row[4],
                    "estimated_time": row[5],
                    "pressure_flg":row[6],
                    "user_id": row[7],
                    "tags": []
                }
            # タグ名があれば追加
            if row[8] is not None:
                todos_dict[todo_id]["tags"].append(row[8])

        todos = list(todos_dict.values())

        return jsonify({
            "message": "successful!!",
            "datas": todos,
        }), 200
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()

def getCompleted_todos():
    user_id = current_user.user_id
    # user_id = 1
    connection = get_connection()
    try:
        cursor = connection.cursor()
        sql = """
            SELECT t.todo_id, t.todo, t.deadline, t.priority, t.finish_flg, t.estimated_time, t.user_id,
                   tg.tag
            FROM todos t
            LEFT JOIN todo_to_tag tt ON t.todo_id = tt.todo_id AND tt.delete_flg = FALSE
            LEFT JOIN tags tg ON tt.tag_id = tg.tag_id
            WHERE t.user_id = %s AND t.finish_flg = TRUE AND t.delete_flg = FALSE
            ORDER BY t.priority DESC, t.deadline ASC
        """
        cursor.execute(sql, (user_id,))
        result = cursor.fetchall()

        todos_dict = {}
        for row in result:
            todo_id = row[0]
            if todo_id not in todos_dict:
                todos_dict[todo_id] = {
                    "todo_id": row[0],
                    "todo": row[1],
                    "deadline": row[2],
                    "priority": row[3],
                    "finish_flg": row[4],
                    "estimated_time": row[5],
                    "user_id": row[6],
                    "tags": []
                }
            if row[7] is not None:
                todos_dict[todo_id]["tags"].append(row[7])

        todos = list(todos_dict.values())

        return jsonify({
            "message": "successful!!",
            "datas": todos,
        }), 200
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()

def getNotYet_todos():
    user_id = current_user.user_id
    # user_id = 1
    connection = get_connection()
    try:
        cursor = connection.cursor()
        sql = """
            SELECT t.todo_id, t.todo, t.deadline, t.priority, t.finish_flg, t.estimated_time, t.user_id,
                   tg.tag
            FROM todos t
            LEFT JOIN todo_to_tag tt ON t.todo_id = tt.todo_id AND tt.delete_flg = FALSE
            LEFT JOIN tags tg ON tt.tag_id = tg.tag_id
            WHERE t.user_id = %s AND t.finish_flg = FALSE AND t.delete_flg = FALSE
            ORDER BY t.priority DESC, t.deadline ASC
        """
        cursor.execute(sql, (user_id,))
        result = cursor.fetchall()

        todos_dict = {}
        for row in result:
            todo_id = row[0]
            if todo_id not in todos_dict:
                todos_dict[todo_id] = {
                    "todo_id": row[0],
                    "todo": row[1],
                    "deadline": row[2],
                    "priority": row[3],
                    "finish_flg": row[4],
                    "estimated_time": row[5],
                    "user_id": row[6],
                    "tags": []
                }
            if row[7] is not None:
                todos_dict[todo_id]["tags"].append(row[7])

        todos = list(todos_dict.values())

        return jsonify({
            "message": "successful!!",
            "datas": todos,
        }), 200
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()

def high_priority():
    user_id = current_user.user_id
    connection = get_connection()
    try:
        cursor = connection.cursor()
        sql = """
            SELECT t.todo_id, t.todo, t.deadline, t.priority, t.finish_flg, t.estimated_time, t.user_id,
                   tg.tag
            FROM todos t
            LEFT JOIN todo_to_tag tt ON t.todo_id = tt.todo_id AND tt.delete_flg = FALSE
            LEFT JOIN tags tg ON tt.tag_id = tg.tag_id
            WHERE t.user_id = %s AND t.priority >= 3 AND t.delete_flg = FALSE
            ORDER BY t.priority DESC, t.deadline ASC
        """
        cursor.execute(sql, (user_id,))
        result = cursor.fetchall()

        todos_dict = {}
        for row in result:
            todo_id = row[0]
            if todo_id not in todos_dict:
                todos_dict[todo_id] = {
                    "todo_id": row[0],
                    "todo": row[1],
                    "deadline": row[2],
                    "priority": row[3],
                    "finish_flg": row[4],
                    "estimated_time": row[5],
                    "user_id": row[6],
                    "tags": []
                }
            if row[7] is not None:
                todos_dict[todo_id]["tags"].append(row[7])

        todos = list(todos_dict.values())

        return jsonify({
            "message": "successful!!",
            "datas": todos,
        }), 200
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()
        
def search_by_tag_and_finish():
    user_id = current_user.user_id
    # user_id = 1 
    connection = get_connection()
    try:
        cursor = connection.cursor()
        data = request.json
        search_tag = data.get("tag")      # 例: "仕事" or None
        finish_flg = data.get("finish_flg")  # True/False/"all" or None

        
        if  search_tag == "all" and finish_flg == "all":
            return getAll_todos()
        elif search_tag == "all" and finish_flg is True:
            return getCompleted_todos()
        elif search_tag == "all" and finish_flg is False:
            return getNotYet_todos()

        # tag指定あり、finish_flg指定なし
        if search_tag and finish_flg == "all":
            # tagのみで絞り込み
            sql = """
                SELECT t.todo_id, t.todo, t.deadline, t.priority, t.finish_flg, t.estimated_time, t.user_id,
                       tg.tag
                FROM todos t
                JOIN todo_to_tag tt ON t.todo_id = tt.todo_id AND tt.delete_flg = FALSE
                JOIN tags tg ON tt.tag_id = tg.tag_id
                WHERE t.user_id = %s
                  AND t.delete_flg = FALSE
                ORDER BY t.priority DESC, t.todo_id ASC
            """
            cursor.execute(sql, (user_id,))
            result = cursor.fetchall()
            todos_dict = {}
            for row in result:
                todo_id = row[0]
                if todo_id not in todos_dict:
                    todos_dict[todo_id] = {
                        "todo_id": row[0],
                        "todo": row[1],
                        "deadline": row[2],
                        "priority": row[3],
                        "finish_flg": row[4],
                        "estimated_time": row[5],
                        "user_id": row[6],
                        "tags": []
                    }
                if row[7] is not None and row[7] not in todos_dict[todo_id]["tags"]:
                    todos_dict[todo_id]["tags"].append(row[7])
            todos = [todo for todo in todos_dict.values() if search_tag in todo["tags"]]
            return jsonify({
                "message": "successful!!",
                "datas": todos,
            }), 200
            # tag指定あり、finish_flg指定なし
        elif search_tag and finish_flg is True:
            # tagのみで絞り込み
            sql = """
                SELECT t.todo_id, t.todo, t.deadline, t.priority, t.finish_flg, t.estimated_time, t.user_id,
                       tg.tag
                FROM todos t
                JOIN todo_to_tag tt ON t.todo_id = tt.todo_id AND tt.delete_flg = FALSE
                JOIN tags tg ON tt.tag_id = tg.tag_id
                WHERE t.user_id = %s
                  AND t.delete_flg = FALSE
                  AND t.finish_flg = TRUE 
                ORDER BY t.priority DESC, t.todo_id ASC
            """
            cursor.execute(sql, (user_id,))
            result = cursor.fetchall()
            todos_dict = {}
            for row in result:
                todo_id = row[0]
                if todo_id not in todos_dict:
                    todos_dict[todo_id] = {
                        "todo_id": row[0],
                        "todo": row[1],
                        "deadline": row[2],
                        "priority": row[3],
                        "finish_flg": row[4],
                        "estimated_time": row[5],
                        "user_id": row[6],
                        "tags": []
                    }
                if row[7] is not None and row[7] not in todos_dict[todo_id]["tags"]:
                    todos_dict[todo_id]["tags"].append(row[7])
            todos = [todo for todo in todos_dict.values() if search_tag in todo["tags"]]
            return jsonify({
                "message": "successful!!",
                "datas": todos,
            }), 200
        elif search_tag and finish_flg is False:
            # tagのみで絞り込み
            sql = """
                SELECT t.todo_id, t.todo, t.deadline, t.priority, t.finish_flg, t.estimated_time, t.user_id,
                       tg.tag
                FROM todos t
                JOIN todo_to_tag tt ON t.todo_id = tt.todo_id AND tt.delete_flg = FALSE
                JOIN tags tg ON tt.tag_id = tg.tag_id
                WHERE t.user_id = %s
                  AND t.delete_flg = FALSE
                  AND t.finish_flg = FALSE 
                ORDER BY t.priority DESC, t.todo_id ASC
            """
            cursor.execute(sql, (user_id,))
            result = cursor.fetchall()
            todos_dict = {}
            for row in result:
                todo_id = row[0]
                if todo_id not in todos_dict:
                    todos_dict[todo_id] = {
                        "todo_id": row[0],
                        "todo": row[1],
                        "deadline": row[2],
                        "priority": row[3],
                        "finish_flg": row[4],
                        "estimated_time": row[5],
                        "user_id": row[6],
                        "tags": []
                    }
                if row[7] is not None and row[7] not in todos_dict[todo_id]["tags"]:
                    todos_dict[todo_id]["tags"].append(row[7])
            todos = [todo for todo in todos_dict.values() if search_tag in todo["tags"]]
            return jsonify({
                "message": "successful!!",
                "datas": todos,
            }), 200

        # tag指定あり、finish_flgも指定
        # ...（今まで通りの処理）...

    except Exception as e:
        print(e)
        return jsonify({
            "error": "検索に失敗しました",
            }), 500
    finally:
        cursor.close()
        connection.close()
# いらない
# def partial_search():
#     # user_id = current_user.user_id
#     user_id = 1
    
#     connection = get_connection()
#     try:
#         cursor = connection.cursor()
#         data = request.json
#         keyword = data.get("keyword")
#         sql = """
#             SELECT t.todo_id, t.todo, t.deadline, t.priority, t.finish_flg, t.estimated_time, t.user_id,
#                    tg.tag
#             FROM todos t
#             LEFT JOIN todo_to_tag tt ON t.todo_id = tt.todo_id AND tt.delete_flg = FALSE
#             LEFT JOIN tags tg ON tt.tag_id = tg.tag_id
#             WHERE t.user_id = %s
#               AND t.delete_flg = FALSE
#               AND t.todo LIKE %s
#             ORDER BY t.priority DESC, t.todo_id ASC
#         """
#         cursor.execute(sql, (user_id, f"%{keyword}%"))
#         result = cursor.fetchall()

#         todos_dict = {}
#         for row in result:
#             todo_id = row[0]
#             if todo_id not in todos_dict:
#                 todos_dict[todo_id] = {
#                     "todo_id": row[0],
#                     "todo": row[1],
#                     "deadline": row[2],
#                     "priority": row[3],
#                     "finish_flg": row[4],
#                     "estimated_time": row[5],
#                     "user_id": row[6],
#                     "tags": []
#                 }
#             if row[7] is not None and row[7] not in todos_dict[todo_id]["tags"]:
#                 todos_dict[todo_id]["tags"].append(row[7])

#         todos = list(todos_dict.values())

#         return jsonify({
#             "message": "successful!!",
#             "datas": todos,
#         }), 200
#     except Exception as e:
#         return jsonify({"error": "検索に失敗しました"}), 500
#     finally:
#         cursor.close()
#         connection.close()
