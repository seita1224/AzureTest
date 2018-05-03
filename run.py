from flask import Flask

app = Flask(__name__)

@app.before_request
def logging_before_request():
    print('before request')

@app.after_request
def logging_after_request(res):
    """ レスポンスが取れる
    res オブジェクトを返す必要がある
    """
    print('after request')
    return res

@app.teardown_request
def logging_end_of_request(exc):
    """ 例外が取れる
    """
    print('end_request')

@app.route('/')
def hello():
    print('request')
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
