from flask import jsonify, request, current_app
from flask_login import current_user
from .db_connection import get_connection
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from pywebpush import webpush, WebPushException
from dotenv import load_dotenv
from flask_login import current_user
import json
import os
import pytz
from .send_email import send_email

load_dotenv()

VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY")
VAPID_CLAIMS = {"sub": "mailto:example@yourdomain.com"}


def check_todos_and_notify():
    print("=== 通知チェックを実行しています ===")
    conn = get_connection()
    cur = conn.cursor()
    tokyo_tz = pytz.timezone('Asia/Tokyo')
    now = datetime.now(tokyo_tz)
    print(f"現在の東京時刻: {now}")

    try:
        # 30分前チェック - 重複チェックなし（何度でも通知可能）
        cur.execute("""
            SELECT t.todo_id, t.todo, t.deadline, u.push_subscription, u.user_id
            FROM todos t
            JOIN users u ON t.user_id = u.user_id
            WHERE t.finish_flg = FALSE
              AND t.delete_flg = FALSE
              AND u.push_subscription IS NOT NULL
              AND t.deadline IS NOT NULL
              AND t.deadline - interval '30 minutes' <= %s
              AND t.deadline - interval '29 minutes' > %s
        """, (now, now))

        rows = cur.fetchall()
        print(f"通知対象のタスク数: {len(rows)}")
        
        for todo_id, todo, deadline, subscription, user_id in rows:
            try:
                print(f"通知送信: ToDo ID {todo_id}, ユーザーID {user_id}, タスク: {todo}, 締切: {deadline}")
                
                # サブスクリプションがJSON形式かチェック
                if subscription:
                    try:
                        subscription_info = json.loads(subscription)
                        print(f"サブスクリプション情報: {subscription_info.keys()}")
                        
                        payload = {
                            "title": "締切30分前",
                            "body": f"{todo} の締切が近いです！"
                        }
                        
                        # プッシュ通知送信
                        webpush(
                            subscription_info=subscription_info,
                            data=json.dumps(payload),
                            vapid_private_key=VAPID_PRIVATE_KEY,
                            vapid_claims=VAPID_CLAIMS
                        )
                        
                        # メール通知送信
                        try:
                            # グローバル変数のflask_appを使用（スケジューラー起動時に設定されたもの）
                            global flask_app
                            if flask_app is None:
                                print("Flaskアプリケーションが設定されていないため、メール送信をスキップします")
                            else:
                                notification_message = "締切30分前の通知"
                                email_sent = send_email(
                                    user_id=user_id, 
                                    todo=todo, 
                                    deadline=deadline, 
                                    alert_message=notification_message,
                                    app=flask_app
                                )
                                if email_sent:
                                    print(f"メール通知送信成功: ToDo ID {todo_id}, ユーザーID {user_id}")
                                else:
                                    print(f"メール通知送信失敗: ToDo ID {todo_id}, ユーザーID {user_id}")
                        except Exception as e:
                            print(f"メール送信中にエラー発生: {e}")
                        
                        
                        # 通知履歴に記録
                        notification_message = "締切30分前の通知"
                        try:
                            notification_sql = """
                            INSERT INTO notifications (todo_id, user_id, message)
                            VALUES (%s, %s, %s)
                            """
                            cur.execute(notification_sql, (todo_id, user_id, notification_message))
                            conn.commit()
                            print(f"通知履歴に記録しました: ToDo ID {todo_id}")
                        except Exception as e:
                            print(f"通知履歴の記録に失敗: {e}")
                            
                        print(f"通知送信成功: ToDo ID {todo_id}")
                    except json.JSONDecodeError:
                        print(f"サブスクリプションのJSONパースエラー: {subscription}")
                else:
                    print(f"ユーザーID {user_id} のサブスクリプションがNULLです")
            except WebPushException as e:
                print(f"通知エラー (ToDo ID {todo_id}): {e}")
            except Exception as e:
                print(f"予期せぬエラー: {e}")
    
    except Exception as e:
        print(f"クエリ実行エラー: {e}")
    finally:
        cur.close()
        conn.close()
        print("=== 通知チェック完了 ===\n")


# スケジューラーとFlaskアプリのインスタンスをグローバル変数として保持
scheduler = None
flask_app = None

# スケジューラーを初期化する関数を定義
# この関数はアプリケーション起動時に呼び出す
def init_scheduler(app=None):
    global scheduler, flask_app
    
    # Flaskアプリインスタンスを保存（通知処理で使用）
    if app is not None:
        flask_app = app
    
    try:
        # スケジューラーがまだ作成されていない場合のみ初期化
        if scheduler is None:
            scheduler = BackgroundScheduler()
            scheduler.add_job(check_todos_and_notify, "interval", minutes=1)
            scheduler.start()
            print("通知スケジューラーが初期化され、起動しました。")
        elif not scheduler.running:
            scheduler.start()
            print("通知スケジューラーが起動しました。")
        else:
            print("通知スケジューラーは既に実行中です。")
    except Exception as e:
        print(f"スケジューラー起動エラー: {e}")



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
        RETURNING notification_id
        """
        cursor = conn.cursor()
        cursor.execute(sql, (todo_id, user_id, message))
        
        # RETURNING句で返されたIDを取得
        result = cursor.fetchone()
        conn.commit()
        
        if result:
            return {"notification_id": result[0], "message": "通知を作成しました"}, 201
        return {"message": "通知を作成しました"}, 201
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()

def read_notification():
    notification_id = request.args.get("notification_id")
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT read_flg FROM notifications WHERE notification_id = %s
        """, (notification_id,))
        row = cursor.fetchone()
        if row and row[0]:
            return jsonify({"message": "すでに既読です"}), 200


        cursor.execute("""
        UPDATE notifications
        SET read_flg = TRUE
        WHERE notification_id = %s
        """, (notification_id,))
        conn.commit()
        return jsonify({"message": "通知を既読にしました"}), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()

def delete_notification():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        user_id = current_user.user_id
        cursor.execute("""
            SELECT COUNT(*) FROM notifications WHERE user_id = %s AND delete_flg = FALSE
        """, (user_id,))
        not_deleted_count = cursor.fetchone()[0]
        if not_deleted_count == 0:
            return jsonify({"message": "履歴はありません"}), 200

        cursor.execute("""
        UPDATE notifications
        SET delete_flg = TRUE
        WHERE user_id = %s
        """, (user_id,))
        conn.commit()
        return jsonify({"message": "通知を削除しました"}), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()

# テスト用の即時通知送信関数
def test_push_notification():
    user_id = current_user.user_id
    
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # ユーザーのサブスクリプション情報を取得
        cur.execute("SELECT push_subscription FROM users WHERE user_id = %s", (user_id,))
        row = cur.fetchone()
        
        if not row or not row[0]:
            return jsonify({"error": "プッシュ通知の登録がありません"}), 400
        
        subscription = row[0]
        
        # テスト通知を送信
        try:
            payload = {
                "title": "テスト通知",
                "body": "これはテスト通知です。正常に届いていれば、プッシュ通知の設定は正常です。"
            }
            
            webpush(
                subscription_info=json.loads(subscription),
                data=json.dumps(payload),
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS
            )
            
            return jsonify({
                "success": True, 
                "message": "テスト通知を送信しました。通知が届いたか確認してください。"
            })
            
        except WebPushException as e:
            print(f"テスト通知エラー: {e}")
            return jsonify({"error": f"通知送信エラー: {str(e)}"}), 500
        except Exception as e:
            print(f"予期せぬエラー: {e}")
            return jsonify({"error": f"予期せぬエラー: {str(e)}"}), 500
            
    except Exception as e:
        print(f"テスト通知クエリエラー: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()