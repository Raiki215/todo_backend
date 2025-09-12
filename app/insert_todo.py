from flask import jsonify, request
from flask_login import current_user, login_required
from google import genai
from dotenv import load_dotenv
from datetime import datetime
import os, re
import json
from .db_connection import get_connection

load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
# client = genai.Client(api_key=api_key)
# today = datetime.now()

def ai_result():
    try:
        # リクエストボディのチェック
        if not request.is_json:
            return jsonify({"error": "JSONリクエストが必要です"}), 400
        data = request.json
        if not data:
            return jsonify({"error": "リクエストボディが空です"}), 400
        # textフィールドのチェック
        if "text" not in data or not data.get("text"):
            return jsonify({"error": "text フィールドが必要です"}), 400
        text = data.get("text")

        # Gemini APIの呼び出し
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
                次の文章をJSONに変換してください。現在日時{today}です。
                フィールド:
                - todo（タスクの内容）
                - deadline（期限、YYYY-MM-DD HH:mm、時間指定がない場合は日付のみ）
                - estimated_time（想定時間、分単位、タスクの内容に応じて合理的に推定）
                - tags（関連するタグの配列、日本語）
                - priority（優先度、1から5の整数、5が最も高い優先度。文章に明示がない場合は Gemini が内容や期限を考慮して決定する）
                ルール:
                - タグが「重要」の場合は priority=5
                - タグが「仕事」の場合は priority=4
                - タグが「健康」の場合は priority=3
                - タグが「私用」の場合は priority=2
                - タグが複数ある場合は、最も優先度が高いタグを採用する
                - タグが上記に当てはまらない場合は Gemini が内容を考慮して 1〜5 で合理的に決定する
                文章:{text}
                必ずJSONのみを出力してください。マークダウンのコードブロック（```）は使用しないでください。
            """
        )

        try:
            response_text = getattr(response, 'text', str(response))
            match = re.search(r'```(?:json)?\s*({.*?})\s*```', response_text, re.DOTALL)
            if match:
                json_text = match.group(1)
            else:
                json_text = response_text.strip()

            result = json.loads(json_text)
            if hasattr(current_user, 'user_id'):
                user_id = current_user.user_id
            else:
                return jsonify({"error": "ユーザーが認証されていません"}), 401

            todo_id = save_todo_with_tags(result, user_id)
            return jsonify({
                "message": "TODOを作成しました",
                "todo_id": todo_id,
                "data": result
            }), 201
        except (json.JSONDecodeError, AttributeError) as e:
            response_text = getattr(response, 'text', str(response))
            return jsonify({
                "error": "AIからの応答をJSONとして解析できませんでした",
                "raw_response": response_text,
                "exception": str(e)
            }), 500
    except Exception as e:
        import traceback
        traceback.print_exc()  # デバッグ用に詳細なエラーを出力
        return jsonify({"error": f"処理中にエラーが発生しました: {str(e)}"}), 500

def save_todo_with_tags(data, user_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        todo = data.get("todo")
        deadline = data.get("deadline")
        estimated_time = data.get("estimated_time")
        tags = data.get("tags", [])
        priority = data.get("priority")

        cursor.execute(
            "INSERT INTO todos (user_id, todo, deadline, estimated_time, priority) VALUES (%s, %s, %s, %s, %s) RETURNING todo_id",
            (user_id, todo, deadline, estimated_time, priority)
        )
        todo_id = cursor.fetchone()[0]
        for tag in tags:
            cursor.execute("SELECT tag_id FROM tags WHERE tag = %s", (tag,))
            tag_row = cursor.fetchone()

            if tag_row:
                tag_id = tag_row[0]
            else:
                cursor.execute("INSERT INTO tags (tag) VALUES (%s) RETURNING tag_id", (tag,))
                tag_id = cursor.fetchone()[0]

            cursor.execute("INSERT INTO todo_to_tag (todo_id, tag_id) VALUES (%s, %s)", (todo_id, tag_id))
        conn.commit()
        return todo_id
    except Exception as e:
        conn.rollback()
        print(f"データベースエラー: {e}")
        # 例外を再スローしてai_result関数でキャッチできるようにする
        raise Exception(f"データベース登録エラー: {e}")
    finally:
        cursor.close()
        conn.close()

def manual_save_todo():
    try:
        data = request.json
        required = ["todo", "deadline", "estimated_time", "tags", "priority"]
        for key in required:
            if key not in data:
                return jsonify({"error": f"{key} フィールドが必要です"}), 400

        tags = data["tags"]
        if isinstance(tags, str):
            tags = [tag.strip() for tag in tags.split(",") if tag.strip()]
            data["tags"] = tags

        user_id = current_user.user_id
        todo_id = save_todo_with_tags(data, user_id)
        return jsonify({
            "message": "手入力TODOを作成しました",
            "todo_id": todo_id,
            "data": data
        }), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"手入力TODO登録エラー: {str(e)}"}), 500