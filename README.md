# TaskFlow Backend - Flask API

Next.js フロントエンドと連携する Flask 製バックエンドです。タスク管理、認証、通知（Push/メール）を提供します。

## 🚀 主な機能

- ユーザー登録/ログイン/ログアウト（Flask-Login）
- タスクの作成・取得・更新・削除
- タグ付けとタグ検索
- プレッシャーモード（pressure_flg の On/Off）
- 完了フラグ（finish_flg）の On/Off、明日へ延期
- 通知履歴の取得/既読/全削除
- Web Push 通知（VAPID）、メール通知（Flask-Mail）

## 🏗️ プロジェクト構成

```
app/
├── __init__.py           # ルーティング・拡張初期化・CORS・LoginManager
├── db_connection.py      # PostgreSQL 接続（環境変数読み込み）
├── models.py             # User モデル（Flask-Login連携）
├── register.py           # /register
├── login.py              # /login, /logout
├── me.py                 # /me（ログインユーザー情報）
├── insert_todo.py        # /insert_todo, /manual_insert_todo
├── get_todos.py          # タスク取得API群
├── edit_todos.py         # 更新API（finish/pressure切替、明日へ、全項目更新）
├── delete_todo.py        # 削除API
├── get_tags.py           # タグ一覧
├── save_subscription.py  # Push購読保存
└── notification.py       # 通知ジョブ・履歴API・テスト通知
run.py                    # エントリポイント（本番/開発の単体起動）
requirements.txt          # 依存パッケージ
```

## 🛠️ 技術スタック

- フレームワーク: Flask 3
- 認証: Flask-Login
- CORS: flask-cors（Cookie 同送対応 supports_credentials=True）
- データベース: PostgreSQL（psycopg2-binary）
- スケジューラ: APScheduler（1 分間隔ジョブ）
- Push 通知: pywebpush + VAPID
- メール: Flask-Mail
- 設定: python-dotenv（.env 読み込み）

## 📦 セットアップ（Windows, PowerShell）

前提: Python 3.10+ / PostgreSQL が利用可能で、接続先 DB にスキーマが用意されていること。

1. 依存関係のインストールと仮想環境

```powershell
# プロジェクト直下で実行（todo_backend フォルダ）
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. 環境変数（.env）

プロジェクト直下に `.env` を作成:

```
# Flask セッション
SECRET_KEY=your_secret_key

# DB 接続
DB_HOST=localhost
DB_USER=postgres
DB_PW=your_password
DB_NAME=your_database

# Web Push (VAPID)
VAPID_PRIVATE_KEY=your_vapid_private_key

# メール送信
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your_smtp_user@example.com
MAIL_PASSWORD=your_smtp_password
```

3. 開発サーバーの起動

```powershell
# PowerShell
venv\Scripts\activate
py run.py
```

- 既定のホスト/ポートは Flask のデフォルトです（http://127.0.0.1:5000）。
- `run.py` は APScheduler を初期化し、アプリ終了時に安全に停止します。
- Cookie 同送が必要なフロントエンドからの呼び出し時は、CORS 設定と SameSite/Secure 設定に留意してください。

## 🌐 主要エンドポイント

- 認証

  - POST /register
  - POST /login
  - POST /logout
  - GET /me

- タスク

  - POST /insert_todo（AI 解析経由）
  - POST /manual_insert_todo（手動作成）
  - GET /get_user_todos（全件）
  - GET /get_user_todos_finished（完了）
  - GET /get_user_todos_yet（未完了）
  - GET /get_user_todos_highpriority（優先度 3 以上）
  - POST /search_by_tag_and_finish（タグ＋完了条件）
  - POST /get_user_todos_update（全項目更新: todo, deadline, priority, estimated_time, tags）
  - POST /get_user_todos_finishflg_update（finish_flg On/Off）
  - POST /pressure_mode_onoff（pressure_flg On/Off）
  - GET /tomorrow_todo（期限を 1 日延期）
  - POST /get_user_todos_delete（削除）

- タグ

  - GET /get_tags

- 通知
  - GET /notification_history
  - GET /read_notification?notification_id=...
  - GET /delete_notification
  - GET /test-notification（Push テスト）
  - POST /save-subscription（Push サブスク保存）

レスポンスは JSON です。各 API はログイン必須（/register, /login, /logout を除く）。

## 🗃️ データモデル（抜粋）

- users: user_id, name, email, password, push_subscription
- todos: todo_id, user_id, todo, deadline, priority, finish_flg, pressure_flg, estimated_time, delete_flg
- tags: tag_id, tag
- todo_to_tag: id, todo_id, tag_id, delete_flg
- notifications: notification_id, todo_id, user_id, message, read_flg, delete_flg, created_at

## 🔐 CORS と Cookie

- `CORS(app, supports_credentials=True)` を設定済み。
- `run.py` では `SESSION_COOKIE_SAMESITE=None` と `SESSION_COOKIE_SECURE=True` を有効化。
- フロントエンドから `fetch` する際は `credentials: 'include'` を付与し、バックエンドのオリジンに合わせてフロントの `NEXT_PUBLIC_API_BASE` を設定してください。

## 🚀 デプロイのヒント

- 本番は Gunicorn などの WSGI サーバー推奨。例:

  ```bash
  # Linux 例（Windows WSL/サーバー上）
  gunicorn -w 2 -b 0.0.0.0:5000 'app:create_app()'
  ```

- 環境変数はサーバー環境に設定（SECRET_KEY/DB/VAPID/MAIL）。
- CORS と Cookie の属性（Secure/SameSite）を本番ドメインに合わせて調整。

## 🩺 トラブルシュート

- DB 接続が None とログに出る

  - .env の DB\_ 変数を確認。接続情報が揃っていないと接続は確立されません。

- CORS/認証で 401 になる

  - ログイン後の Cookie が送られているかを確認（credentials: 'include'）。
  - SESSION*COOKIE*\* 設定とフロント/バックのオリジン一致を確認。

- プッシュ通知が届かない

  - `VAPID_PRIVATE_KEY`、`/save-subscription` の保存可否、ブラウザの通知許可を確認。

- メールが送れない
  - MAIL\_\* の値と SMTP 到達性、ポート/TLS 設定を確認。

## 📝 ライセンス / 🤝 コントリビューション

- MIT License（フロントと同様）
- コントリビュート手順はフロント README に準拠。PR を歓迎します。
