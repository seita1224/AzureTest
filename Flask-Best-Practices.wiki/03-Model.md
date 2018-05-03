モデル層の設計は Flask の extension を用いると確実に、かつ早く作成することが出来るでしょう。ここでは、 Redisを直接使う, MongoEngine, SQLAlchemy などの ORM を使う方法を簡単にまとめておきます。下記のディレクトリ構成を想像してください。

```
    application/
        |- app/
            |- __init__.py
            |- models/
                |- __init__.py
                |- sa_user.py
                |- me_user.py
                |- session.py
```

```
# app/__init__.py
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.sqlalchemy import SQLAlchemy
from redis import Redis

app = Flask(__name__)
mongo = MongoEngine(app)
sa = SQLAlchemy(app)
redis = Redis()
app.redis = redis

```

### SQLAlchemy
SQLAlchemy は言わずと知れた python 製の ORM です。学習コストは極めて高いですが、使いこなせればソースコードは相当量圧縮できるでしょう。 Flask から使うには実際には Flask-SQLAlchemy を用いて以下の様に設計します。

created_at, updated_at をデフォルトで入るように設計するのはいいことです。一般的なものは Base クラスに切り出し、それを継承するような設計をとりましょう。一覧検索系などは classmethod で実装するのが一般的です。後の拡張は SQLAlchemy を勉強して拡張してくのがいいでしょう。

```
# app/models/sa_user.py
from app import sa

class Base(sa.Model):
    created_at = sa.Column(sa.DateTime)
    updated_at = sa.Column(sa.DateTime)

    def __init__(self):
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

class SAUser(Base):

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(128))
    email = sa.Column(sa.String(128))
    age = sa.Column(sa.Integer, index=True)
    sex = sa.Column(sa.String(1))

    @classmethod
    def fetch_30_age(cls):
        return cls.query.filter(age == 30).all()
    
    def change_sex(self, sex=None):
        self.sex = sex
```

### MongoEngine
MongoEngine は MongoDB 社純正の python 向け ODM です。基本的なやり方は SQLAlchemy とほとんど同じです。実際には Flask-mongoengine を用いて以下の様に書きます。

```
# app/models/me_user.py
from app import mongo

class Base(mongo.Document):
    created_at = mongo.DateTimeField()
    updated_at = mongo.DatetimeField()

class MEUser(Base):
    id = mongo.StringField()
    name = mongo.StringField()
    email = mongo.EmailField()
    sex = mongo.StringField()
    age = mongo.IntField()

    @classmethod
    def fetch(cls):
        pass
```

### Redis
Redis は ランキングの実装や、セッション、キャッシュなどによく使われる構造型 DB です。flask の extension の star 数があまりにも少ないため、pyredis を持ちた方がいいでしょう。また、 app.redis を設定しているので、 current_app を用いて redis を索引することができます。

```
from flask import current_app

class Session(object):
    def __init__(self):
        self.redis = current_app.redis

    def get(self, key):
        return self.redis.get(key)
        
    def save(self, key, value):
        self.redis.set(key, value)
```