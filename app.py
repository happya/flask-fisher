from flask import Flask
__author__ = 'yyi'
app = Flask(__name__)



@app.route('/')
def hello_world():
    # class-based view
    return 'Hello World!'

# app.add_url_rule('/', view_func=hello_world)

if __name__ == '__main__':
    app.run(debug=True)
