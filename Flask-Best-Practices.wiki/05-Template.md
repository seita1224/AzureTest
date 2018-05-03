Flask でのフロントエンド開発の方法は多岐に渡ります。テンプレートレンダリングでシンプルに作る方法、直接HTMLを返す方法、シングルページアプリケーションとして、 Ajax を通して API と javascript を対話させる方法などがあります。ここでは最もシンプルなテンプレートエンジン、特に jinja2 を用いた基本的なページ作成方法を説明します。

### 基本的な templates
Flask には jinja2 というテンプレートエンジンが同時に付属されています。 API サーバを作るには不要の テンプレートエンジンですが、管理画面の作成、ランディングページ、サービスダウンのメンテナンス告知など、知っておいて損は無いので簡単に説明します。ディレクトリ構成は以下の用になりますが、Flask インスタンス化の際の設定で変更が可能です。 なお、 React や Angular を用いる場合は static の内容を bower で管理させたり、独自のディレクトリ構造に変化します。その際はサーバサイドとクライアントサイドのリポジトリを分けて、デプロイの際に一度全体のビルド処理を挟むといいでしょう。

```
ディレクトリ構成
    application/
        |- app.py
        |- static/
            |- js/
            |- css/
                |- base.css
            |- img/
        |- templates/
            |- base.html
            |- sub.html
```

```
# app.py
from flask import Flask, render_template

app = Flask(__name__,
    static_folder='static',      # 静的ファイルのディレクトリ
    templates_folder='templates' # テンプレートのディレクトリ
)

@app.route('/')
def index():
   param = dict(a=10, b=20)
   return render_template('sub.html', param=param)
app.run()
```

```
templates/base.html
<html>
    <link href="{{ url_for('static', filename='css/base.css') }}" rel="stylesheet">
    <title> Flask Best Practices </title>
    {% bock the_contents %} <!-- 継承先の名前を入れておく -->
    {% endblock %}
</html>
```

```
templates/sub.html
{% extends 'base.html' %} 
{% block the_contents %}
    <p> {{ param['a'] }} </p> <!-- 変数を埋め込む -->

    {% for key, value in param.items() %} <!-- python シンタックスでコード埋め込み -->
         <p>{{key}}, {{value}}</p>
    {% endfor %}
{% endblock %}
```

### context processor
jinja2 は　```{{}}```で囲まれた部分が埋め込みになりますが、この部分にアプリケーション毎に独自の関数を定義することが出来ます。 Angular.js や  React.js のカスタムディレクティブ、に近い概念です。

```
# app.py

from flask import Flask

app = Flask(__name__)

@app.context_processor
def some_processor():
   def email(name, domain):
       return "{0}@{1}".format(name, domain)
   return email
```

```
# index.html
# サーバで定義されたプロセッサが使える
<p> {{ email('foo', 'test.com') }} </p>
```

### custom filter
jinja2 も Angular, React 同様にフィルター機能を独自に定義することができます。

```
from flask import Flask

app = Flask(__name__)

@app.template_filter('lastname')
def lastname_filter(name):
    return name.split(' ')[-1]
```

```
templates/index.html
<p>{{ name|lastname }}</p> <!-- name はサーバから返されたパラメータ -->
```

### テンプレートを超えて
flask-bootstrap なるものを持ちれば実は 上記 templates をもっと簡単に定義することが出来ます。しかし、フロントエンドにもっと気を使う方向で考えている場合、 SPA + フロントエンドフレームワークの導入を検討したほうがいい場合が多いです。(クライアントの専門家と仕事の分担が簡単、バックエンドに依らないので大規模な変更の影響範囲を小さく出来る) React.js が最近の流行りですので、一考。