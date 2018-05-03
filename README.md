ディレクトリ構成  

    |- application
        |- server.py              # サーバの起動スクリプト
        |- config/                # 設定ファイル
            |- __init__.py
        |- app/
            |- __init__.py
            |- models/
            |- views/
            |- statics/            # 静的ファイル
                |- css/
                |- js/
            |- templates/
            |- models/
            |- views/
        |- venv/                   # pyvenv 環境 gitignore しましょう
            |- lib/
            |- bin/
            |- include/

 