"""
author: yyi
description: entrance file
"""
from app import create_app

app = create_app()

# @app.route('/')
# def hello_world():
#     headers = {
#         'content-type': 'text/html'
#     }
#     response = make_response('<html></html>', 404)
#     response.headers = headers
#     # class-based view
#     return response

# app.add_url_rule('/', view_func=hello_world)
# app.run(debug=app.config['DEBUG'])


if __name__ == '__main__':
    # only run in this file, if this file is imported as module, will not execute
    # production environment, need use nginx + uwsgi(web server)
    # ensure this will not run in production environment
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=5011)
