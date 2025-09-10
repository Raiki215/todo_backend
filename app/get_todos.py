from .db_connection import get_connection
from flask import jsonify

# 優先度の降順、期限の昇順
# 全てのタスクを表示
def getAll_todos(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'select * from todos where user_id = %s order by priority desc , deadline ASC'
    cursor.execute(sql,(user_id,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify({
        "message":result
    })

#完了済みのタスクを優先度の降順で表示
def getCompleted_todos(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'select * from todos where user_id = %s and finish_flg = TRUE order by priority desc , deadline ASC'
    cursor.execute(sql,(user_id,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({
        "message":result
    })

# 未完了のタスクを優先度の降順で表示
def getNotYet_todos(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'select * from todos where user_id = %s and finish_flg = FALSE order by priority desc , deadline ASC'
    cursor.execute(sql,(user_id,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({
        "message":result
    })

# 優先度の高い物だけ
def high_priority(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'select * from todos where user_id = %s and finish_flg = FALSE and priority >= 3 order by priority desc , deadline ASC'
    cursor.execute(sql,(user_id,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({
        "message":result
    })