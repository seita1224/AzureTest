ディレクトリ構成  

    |- application
        |- server.py              # サーバの起動スクリプト
        |- tasks.py               # バッチのインターフェースやタスクランナーを記述
        |- tools/                 # バッチや、CLIツールをココに
        |- config/                # 設定ファイル
            |- __init__.py
            |- development.py
            |- production.py
        |- app/
            |- __init__.py
            |- models/
            |- views/
            |- statics/            # 静的ファイル
                |- css/
                |- js/
                |- img/
            |- templates/
        |- migrations/             # flask-alembic を用いる場合の migration ファイル
        |- tests/                  # noseテスト モデルとビューとモックデータ
            |- models/
            |- views/
            |- mocks/
        |- venv/                   # pyvenv 環境 gitignore しましょう
            |- lib/
            |- bin/
            |- include/
            |- man/

 