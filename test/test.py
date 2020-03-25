from flask import Flask, current_app

app = Flask(__name__)

with app.app_context():
    a = current_app
    d = current_app.config['DEBUG']

# with clause: if an object implements context protocol, can use with
# context manager
# __enter__, __exit__
# with: context expression
# context expression must return a context manager

# eg:
# 1. connect database: __enter__
# 2. query execution: codes
# 3. release resource: __exit__


# class A:
#     def __enter__(self):
#         a = 1
#         return self
#     def query(self):
#         print('query')
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print('close')
#         return True



# with A() as obj_A:
#     """
#        obj_A: return by __enter__
#     """
#       obj_A.query()
#     pass