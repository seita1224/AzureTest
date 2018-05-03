from flask.views import MethodView
from flask import Flask

app = Flask(__name__)

def middleware(func):
    def deco(*args, **kwargs):
        print('middleware')
        return func(*args, **kwargs)
    return deco

class Resource(MethodView):
    decorators = [middleware]

    def get(self, id=None):
        if not id: return 'index'
        return 'show'

    def post(self):
        return 'create'

    def put(self, id):
        return 'update'

    def delete(self, id):
        return 'delete'

resource_view = Resource.as_view('resource')
app.add_url_rule('/resource', view_func=resource_view, methods=['GET', 'POST'])
app.add_url_rule('/resource/<int:id>', view_func=resource_view, methods=['GET', 'PUT', 'DELETE'])

app.run()
