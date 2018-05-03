これから記述する内容は flask フレームワークの真髄とも言える Blueprint の概念です。

flask は基本的にマイクロフレームワークであり、モノリシックな大きいアプリケーションを作るフルスタックフレームワーク
ではありません。しかしながら、モジュール化されたマイクロサービスを組み合わせる事で、
大規模なアプリケーションを構築するための手段が用意されています。
そのモジュール化されたマイクロサービスが Blueprint です。

Blueprint は　　Flask オブジェクトの雛形になるようなもので、 Flask が持っているメソッドをすべて
持っているとは限りません。しかしながら基本的なルーティングに関しては備えているので、
Blueprint モジュールでルーティングの設定、 DB のモデルスキーマの設定、 テンプレートの記述
などが可能です。

例えば、次のような記述の仕方をします。
```
    application/
      |- app.py
      |- micro/
          |- __init__.py
```

```
# micro/__init__.py
from flask import Blueprint

micro = Blueprint('micro', __name__, url_prefix='/micro')

@micro.route('/')
def attachement():
    return 'this is micro service (/micro)'
```

```
# app.py
from flask import Flask
from micro import micro

if __name__ == '__main__':
    app.register_blueprint(micro)
    app.run(host='0.0.0.0')
```

しかし、 Blueprint の真髄は関心事を完全に分離できることにあります、このマイクロアプリケーションを別サービスとして切り出してしまいましょう。
理想的には、 gitで別リポジトリで管理された Blueprint をメインの Flask アプリケーションに pip コマンドで取り込む
ことができれば、完全なサービスの使い回しができる事になります。再利用の際は上記の register_blueprint 関数を呼び出す
だけです。

pip でインストールできるようにするには、 setup.py を リポジトリのルートに用意する必要があります。ここでは、試しにユーザーの登録情報
を MongoEngine という MongoDB の ORM を用いてモデル化し、その機能をメインのアプリケーションにマウントする場合を例にとりましょう。

```
    flask-mod-user/
      |- setup.py
      |- app/
         |- __init__.py
```

```
# setup.py
from setuptools import setup, find_packages

setup(
    name='user',
    version='1.0',
    license='MIT',
    author='Yoshiya Ito',
    author_email='myon53@gmail.com',
    description='user micro module',
    packages=find_packages(),
    platforms='any',
    install_requires=[
        'flask',
        'mongoengine'
    ],
    classifiers=[
    ]
)
```

```
#app/__init__.py

from flask.ext.mongoengine import MongoEngine

db = MongoEngine()
user = Blueprint('user', __name__, url_prefix='/user')

class User(db.Document):
    name = db.StringFiled(max_length=128, required=True)
    password = db.StringField(max_length=128, required=True)
    device_key = db.StringField(max_length=128, required=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def some_function(self):
        return 'something'

    @classmethod
    def fetch_all(cls):
        ''' 全部取得する関数
        '''
        return cls.objects()

@user.route('/', ['GET'])
def index():
    return User.fetch_all()

@user.route('/<int:id>', ['GET'])
def show(id):
    user = User.objects.get(id=id)
    return user

@user.route('/', ['POST'])
def create():
    user = User(name='hoge', password='hoge', device_key='123')
    user.save()
    return user

@user.route('/<int:id>', ['PUT'])
def update(id):
    user = User.objects.get(id=id)
    user.name = 'new name'
    return user

@user.route('/<int:id>', ['DELETE'])
def delete(id):
    user = User.objects.get(id=id)
    user.delete()
    return {}

```

あとは作成したこのモジュールを git から clone し、 ``` pip isntall . ``` とすることで現在の python の環境に自作のモジュールがインストールできます。(pyvenv を activate している場合はその libs 以下) また、これらマイクロモジュールの書き方は特に指定が有るわけでは無いので自由に作成が可能です。Blueprint オブジェクトを通してアプリケーションをルーティングすることだけ気をつけてください。しかしながら、やはりモジュールも REST-API の原則に従っていることが推奨されます。実際 Blueprint オブジェクトにも flask-restfull プラグインを適用して設計することが可能です。(ルーティングの決定が遅延されるため)

考察すべき点として、 db = MongoEngine オブジェクトが作成された時点でコネクションが発生するのではないかという懸念がありますが、ソースを調べたら、　init_app まで遅延されるので問題無いです。 また、マイクロモジュールで作成された db.Document クラスと メインモジュールで作成するであろう db.Document クラスは全くの同一になるはずなので、オブジェクトの参照が異なる事による弊害は発生しません。あとは requirements.txt に git 指定で
マイクロモジュールを設定すれば、メインのモジュールで、一般的なライブラリを使う感覚でモジュールを import し、 register すれば既に user の機能が完成している状態になります。