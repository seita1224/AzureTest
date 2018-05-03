flask を用いて Restful-API を構築するには、いくつかの方法があります。一つは、```@app.route()``` 関数デコレータを用いて
ルーティングを直接指定する方法。二つ目はクラスを用いて設定する方法。最後に flask-restfull プラグインを用いる方法です。
ここでは体系的にそれぞれどのようなコードの書き方になるのかを紹介します。

### 関数デコレータベースの方法

関数デコレータベースでの構築方法は単純で、 Flask オブジェクトを作成し、そのオブジェクトの持つデコレータメソッドを
対象の任意の関数にアタッチしていく方法です。 以下では一般的な REST の規則に従ったルーティングの方法と、それでは
賄うことが出来ないような特殊な場合を列挙した実例を示しています。 ```/resource```というリソースがあったとして、
その一覧、詳細、作成、更新、削除を行える用にしています。プレースホルダの```<int:id>```は、リソースのURI自体に
パラメータが含まれる場合に利用します。その際、指定できる型として、 int, float, path があります。詳しくは flask ドキュメント
を参照してください。一般的には int しか使いません。
一つの関数に二つのデコレータをアタッチすることもできます。この際、デコレータに一致したルーティング全てに対してこのメソッド
を呼ぶようになります。

```
#__init__.py

from flask import Flask

app = Flask()

@app.route('/resource', methods=['GET'])
def index():
    """ リソースの一覧
    """
    return 'index'

@app.route('/resource/<int:id>', methods=['GET'])
def show(id):
    """ リソースの詳細情報
    """
    return 'show'

@app.route('/resource', methods=['POST'])
def create():
    """ リソースの作成
    """
    return 'create'

@app.route('/resource/<int:id>', methods=['PUT'])
def update(id):
    """ リソースの更新
    """
    return 'update'

@app.route('/resource/<int:id>', methods=['DELETE'])
def delete(id):
    """ リソースの削除
    """
    return 'delete'

@app.route('/resource/special', methods=['GET', 'POST'])
@app.route('/resource/other', methods=['POST'])
def special():
    """ 特殊なルーティング
    """
    return 'special'

if __name__ == '__main__':    
    app.run()
```

### クラスベースの方法

クラスベースのルーティング方法は、 View クラス、または MethodView クラスのサブクラスを用いて作成します。 View を用いた方法は見た目が
汚いため、あまり推奨しません。興味のある人は Flask のドキュメントを参照してください。ここでは MethodView を用いた方法を強く推奨するので、
以下にその方法をコードベースで紹介します。

```
#__init__.py

from flask import Flask
from flask.views import MethodView

app = Flask()

class OtherResource(MethodView):
    
    def get(self, id=None):
        if not id:
            return 'index'
        return 'show'
    
    def post(self):
        return 'create'

    def put(self, id):
        return 'update'
    
    def delete(self, id):
        return 'delete'

other_resource = OtherResource.as_view('other_resource')
app.add_url_rule('/other', view_func=other_resource, methods=['GET', 'POST'])
app.add_url_rule('/other/<int:id>', view_func=other_resource, methods=['GET', 'PUT', 'DELETE'])

if __name__ == '__main__':
    app.run()
```

### flask-restful を用いた方法

これまでの方法は flask のデフォルトの機能ですべて実装できますが、より良い、RESTful な API を作成するための方法として、 flask-restfulを
紹介します。このプラグインを用いた場合、体系的にパラメータのバリデーションを行ったり、より綺麗なルーティング、エラーハンドリング、ミドルウェアの設計が可能になります。```pip install flask-restful``` で環境に flask-restful をインストールしてください

```
# __init__.py

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class SomeResource(Resource):

    def get(self, id=None):
         if not id: return 'index'
         return 'show'
    
    def post(self):
        return 'create'
    
    def put(self, id):
        return 'update'
    
    def delete(self, id):
        return 'delete'

api.add_resource(SomeResource, 'resource/<int:id>')

if __name__ == '__main__':
   app.run()
```

以上を Views ディレクトリを作成し、切り出す事で、綺麗な MTV 構造が作成できます。

```
    application/
        |- __init__.py
        |- app/
            |- __init__.py
            |- views/
                |- __init__.py
                |- user.py
                |- other_view.py
```