from app import create_app
from flask_login import login_user, logout_user, login_required, current_user
from app.notification import scheduler  # スケジューラーのインスタンスをインポート（初期化後に取得）
import os
import atexit


app = create_app()
app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config['SESSION_COOKIE_SECURE'] = True

# アプリケーション終了時にスケジューラーを停止する
@atexit.register
def shutdown_scheduler():
    from app.notification import scheduler  # 最新のスケジューラーインスタンスを取得
    if scheduler and scheduler.running:
        scheduler.shutdown()
        print("通知スケジューラーを停止しました。")

if __name__ == "__main__":
    try:
        # デバッグモードをFalseにすることで、アプリが2回起動する問題を回避
        # 開発中にコードを変更してリロードするには、手動でアプリを再起動する必要がある
        app.run(debug=False)
    except (KeyboardInterrupt, SystemExit):
        # Ctrl+CなどでFlaskサーバーが停止した場合にもスケジューラーを確実に停止
        print("サーバー停止: スケジューラーを終了します...")
        from app.notification import scheduler  # 最新のスケジューラーインスタンスを取得
        if scheduler and scheduler.running:
            scheduler.shutdown()