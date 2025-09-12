from flask_login import current_user
from .db_connection import get_connection
from flask import jsonify


def getAll_todos():
    user_id = 3 # 仮
    connection = get_connection()
    try:
        cursor = connection.cursor()
        sql = """
            SELECT t.todo_id, t.todo, t.deadline, t.priority, t.finish_flg, t.estimated_time, t.user_id,
                   tg.tag_id, tg.tag
            FROM todos t
            LEFT JOIN todo_to_tag tt ON t.todo_id = tt.todo_id AND tt.delete_flg = FALSE
            LEFT JOIN tags tg ON tt.tag_id = tg.tag_id
            WHERE t.user_id = %s AND t.delete_flg = FALSE
            ORDER BY t.priority DESC, t.todo_id ASC
        """
        cursor.execute(sql, (user_id,))
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

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
            # タグがあれば追加
            if row[7] is not None and row[8] is not None:
                todos_dict[todo_id]["tags"].append({
                    "tag_id": row[7],
                    "tag": row[8]
                })

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


# 完了済みのタスクを優先度の降順で表示（タグ情報も含める）
def getCompleted_todos():
    user_id = 1 # 仮
    connection = get_connection()
    try:
        cursor = connection.cursor()
        sql = """
            SELECT t.todo_id, t.todo, t.deadline, t.priority, t.finish_flg, t.estimated_time, t.user_id,
                   tg.tag_id, tg.tag
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
            if row[7] is not None and row[8] is not None:
                todos_dict[todo_id]["tags"].append({
                    "tag_id": row[7],
                    "tag": row[8]
                })

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

# 未完了のタスクを優先度の降順で表示（タグ情報も含める）
def getNotYet_todos():
    user_id = 1 # 仮
    connection = get_connection()
    try:
        cursor = connection.cursor()
        sql = """
            SELECT t.todo_id, t.todo, t.deadline, t.priority, t.finish_flg, t.estimated_time, t.user_id,
                   tg.tag_id, tg.tag
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
            if row[7] is not None and row[8] is not None:
                todos_dict[todo_id]["tags"].append({
                    "tag_id": row[7],
                    "tag": row[8]
                })

        todos = list(todos_dict.values())

        return jsonify({
            "message": "successful!!",
            "datas": todos,
        }), 200
    except Exception as e:
        print(e)
        
# 優先度3以上のタスクを表示（タグ情報も含める）
def high_priority():
    user_id = 1 # 仮
    connection = get_connection()
    try:
        cursor = connection.cursor()
        sql = """
            SELECT t.todo_id, t.todo, t.deadline, t.priority, t.finish_flg, t.estimated_time, t.user_id,
                   tg.tag_id, tg.tag
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
            if row[7] is not None and row[8] is not None:
                todos_dict[todo_id]["tags"].append({
                    "tag_id": row[7],
                    "tag": row[8]
                })

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
        
# 優先度の降順、todo_idの昇順
# 全てのタスクを表示
# def getAll_todos():
#     user_id = 1#仮　↓で書き直す
#     # user_id = current_user.user_id
#     connection = get_connection()
#     try:
#         cursor = connection.cursor()
#         # sql = "select * from todos where user_id = %s and delete_flg = FALSE order by priority desc , todo_id ASC"
#         sql = """
#             SELECT *  FROM todos t
#             LEFT JOIN
#             todo_to_tag tt ON t.todo_id = tt.todo_id AND tt.delete_flg = FALSE
#             LEFT JOIN
#             tags tg ON tt.tag_id = tg.tag_id
#             WHERE
#             t.user_id = %s
#             AND t.delete_flg = FALSE
#             ORDER BY
#             t.priority DESC,
#             t.todo_id ASC
#             """
#         cursor.execute(sql,(user_id,))
#         result = cursor.fetchall()
        
#         columns = [desc[0] for desc in cursor.description]
#         datas = [dict(zip(columns, row)) for row in result]
#         print(datas)

#         return jsonify({
#             "message":"successful!!",
#             "datas": datas,
#         }),200
#     except Exception as e:
#         print(e)
#     finally:
#         cursor.close()
#         connection.close()        

# #完了済みのタスクを優先度の降順で表示
# def getCompleted_todos():
#     user_id = 1#仮　↓で書き直す
#     # user_id = current_user.user_id
#     connection = get_connection()
#     try:
#         cursor = connection.cursor()
#         sql = "select * from todos where user_id = %s and finish_flg = TRUE and delete_flg = FALSE order by priority desc , deadline ASC"
#         cursor.execute(sql,(user_id,))
#         result = cursor.fetchall()
        
#         columns = [desc[0] for desc in cursor.description]
#         datas = [dict(zip(columns, row)) for row in result]
#         print(datas)

#         return jsonify({
#             "message":"successful!!",
#             "datas": datas,
#         }),200
#     except Exception as e:
#         print(e)
#     finally:
#         cursor.close()
#         connection.close()


# # 未完了のタスクを優先度の降順で表示
# def getNotYet_todos():
#     user_id = 1#仮　↓で書き直す
#     # user_id = current_user.user_id
#     connection = get_connection()
#     try:
#         cursor = connection.cursor()
#         sql = "select * from todos where user_id = %s and finish_flg = FALSE and delete_flg = FALSE order by priority desc , deadline ASC"
#         cursor.execute(sql,(user_id,))
#         result = cursor.fetchall()
#         cursor.execute("select",())
        
#         columns = [desc[0] for desc in cursor.description]
#         datas = [dict(zip(columns, row)) for row in result]
#         print(datas)

#         return jsonify({
#             "message":"successful!!",
#             "datas": datas,
#         }),200
#     except Exception as e:
#         print(e)
#     finally:
#         cursor.close()
#         connection.close()


# 優先度の高い物だけ
# def high_priority():
#     user_id=1
#     # user_id = current_user.user_id
#     connection = get_connection()
#     try:
#         cursor = connection.cursor()
#         sql = "select * from todos where user_id = %s and finish_flg = FALSE and delete_flg = FALSE and priority >= 3 order by priority desc , deadline ASC"
#         cursor.execute(sql,(user_id,))
#         result = cursor.fetchall()
#         columns = [desc[0] for desc in cursor.description]
#         datas = [dict(zip(columns, row)) for row in result]
#         print(datas)

#         return jsonify({
#             "message":"successful!!",
#             "datas": datas,
#         }),200
#     except Exception as e:
#         print(e)
#     finally:
#         cursor.close()
#         connection.close()