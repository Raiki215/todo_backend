
from flask import Flask, request, jsonify
from flask_login import current_user, login_required
import json
from .db_connection import get_connection

def save_subscription():
    data = request.json
    user_id = current_user.user_id
    
    # データ構造のチェックとロギング
    print("受信したサブスクリプションデータ:", data)
    
    try:
        # データ形式が直接subscription自体かsubscriptionをキーに持つオブジェクトか確認
        if "subscription" in data:
            subscription = data["subscription"]
        else:
            subscription = data
        
        # オブジェクトをJSON文字列に変換
        subscription_json = json.dumps(subscription)
        
        conn = get_connection()
        cur = conn.cursor()
        
        # 更新前の確認
        cur.execute("SELECT push_subscription FROM users WHERE user_id=%s", (user_id,))
        before = cur.fetchone()
        print(f"更新前のサブスクリプション: {before[0] if before and before[0] else 'None'}")
        
        # サブスクリプション更新
        print(f"ユーザーID {user_id} のサブスクリプションを更新します")
        cur.execute("UPDATE users SET push_subscription=%s WHERE user_id=%s",
                    (subscription_json, user_id))
        conn.commit()
        
        # 更新後の確認
        cur.execute("SELECT push_subscription FROM users WHERE user_id=%s", (user_id,))
        after = cur.fetchone()
        print(f"更新後のサブスクリプション: {after[0] if after and after[0] else 'None'}")
        
        cur.close()
        conn.close()
        return jsonify({"success": True, "message": "サブスクリプションが保存されました"})
    except Exception as e:
        print("サブスクリプション保存エラー:", e)
        return jsonify({"success": False, "error": str(e)}), 500