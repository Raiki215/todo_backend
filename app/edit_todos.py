from .db_connection import get_connection
from flask import request, jsonify, session
from flask_login import current_user

def edit_todo_all():
    try:
        data = request.json
        todo_id = data.get("todo_id")
        todo = data.get("todo")
        deadline = data.get("deadline")
        priority = data.get("priority")
        # finish_flg = data.get("finish_flg")
        estimated_time = data.get("estimated_time") 
        # delete_flg = data.get("delete_flg") 
        tags = data.get("tags",[])
        # user_id = data.get("user_id") 
        
        required = ["todo", "deadline", "estimated_time", "tags", "priority"]
        for key in required:
            if key not in data:
                return jsonify({"error": f"{key} フィールドが必要です"}), 400
    except Exception as e:
        print(f"error : {e}")
        return jsonify({
            "error":"error!"
        })
    
    #文字数やデータ型などのチェックを入れる
    #js側のバリデーションチェックがまだないのでできるところまでやる
    connection = get_connection()
    try:
        cursor = connection.cursor()
        sql = """
        update todos set todo = %s, deadline = %s, priority = %s, estimated_time = %s
        where todo_id = %s and delete_flg = FALSE
        """
        cursor.execute(sql,(todo, deadline, priority, estimated_time, todo_id,))
        connection.commit()
        
        # tagsは文字列
        #タグlist　空白除去
        new_tag_list = [item.strip() for item in tags.split(",")]
        new_tag_id_list = []
        # タグが既存でない場合はどうするか
        # tagの文字列からidを検索　→　idをlistに格納
        for i in new_tag_list:
            cursor.execute("select tag_id from tags  where tag = %s", (i,))
            tag_id = cursor.fetchone()
            if tag_id is None:
                print("存在しないタグの時は追加する処理の呼び出し")
                # 今回は仮で1
                tag_id = 1
                # continue
            else:
                new_tag_id_list.append(tag_id[0])
            
        # listをセットにし重複を排除 → listに戻し（ソートは一応）
        # new_tag_id_list =  set(new_tag_id_list)
        new_tag_id_list = sorted(set(new_tag_id_list))
        
        #新旧タグの比較
        cursor.execute("select tag_id from todo_to_tag where todo_id = %s and delete_flg = FALSE",(todo_id,))
        now_tag = cursor.fetchall()
        # delete_flgはtrueだが過去にこのtodoについていたタグ
        cursor.execute("select tag_id from todo_to_tag where todo_id = %s and delete_flg = TRUE",(todo_id,))
        df_now_tag = cursor.fetchall()

        now_tag_list = [tag[0] for tag in now_tag]  # タプルからIDだけ抽出
        df_now_tag_list = [dtag[0] for dtag in df_now_tag]

        # 追加するタグID（new_tag_id_listにあってnow_tag_listにないもの）
        add_tag_list = [tag_id for tag_id in new_tag_id_list if tag_id not in now_tag_list]
        
        # 復活させるタグID
        revival_tag_list = [tag_id for tag_id in new_tag_id_list if tag_id in df_now_tag_list]

        # 削除するタグID（now_tag_listにあってnew_tag_id_listにないもの）
        del_tag_list = [tag_id for tag_id in now_tag_list if tag_id not in new_tag_id_list]
        
        # 削除
        for delflgTagid in del_tag_list:
            cursor.execute("update todo_to_tag set delete_flg = TRUE where tag_id = %s and todo_id = %s",(delflgTagid,todo_id))
            connection.commit()
            
        # 復活
        for revflgTagid in revival_tag_list:
            cursor.execute("update todo_to_tag set delete_flg = FALSE where todo_id = %s and tag_id = %s",(todo_id, revflgTagid))
            connection.commit()
            
        # 追加
        # for addflgTagid in add_tag_list:
        #     cursor.execute("insert into todo_to_tag(todo_id, tag_id) values(%s, %s)",
        #                    (todo_id, addflgTagid,))
        #     connection.commit()
        
        for addflgTagid in add_tag_list:
            cursor.execute(
                "select id from todo_to_tag where todo_id = %s and tag_id = %s",
                (todo_id, addflgTagid)
            )
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(
                    "insert into todo_to_tag(todo_id, tag_id) values(%s, %s)",
                    (todo_id, addflgTagid,)
                )
                connection.commit()
            
            
        return jsonify({
            "message" : "todos Update completed.",
            "todo_id": todo_id,
            "data" : data,
            
        }),200
    except Exception as e:
        print(e)
        return jsonify({
            "message": "error",
            "aaaa":addflgTagid
        })
    finally:
        cursor.close()
        connection.close()
        
def finish_flg_OnOff():
    connection = get_connection()
    try:
        
        cursor = connection.cursor()
        data = request.json
        todo_id = data.get("todo_id")
        # finish_flg = data.get("fininsh_flg")
        cursor.execute("UPDATE todos SET finish_flg = NOT finish_flg WHERE todo_id = %s", (todo_id,))
        connection.commit()
        cursor.execute("select finish_flg from todos where todo_id = %s",(todo_id,))
        finish_flg = cursor.fetchone()[0]

        if finish_flg:
            msg = f"successful !! This todo Completed !! :)"
        else:
            msg = f"successful !! This todo status has been restored."
            
        
        return jsonify({
            "message" : msg,
            "todo_id": todo_id,
            "finish_flg":finish_flg,
        }),200
    except Exception as e:
        return jsonify({
            "error" : "Could not update the this todos finish_flg "
        }),500