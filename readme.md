# flask
> unique url

## register a route

- use python decorator, for example
```python
@app.route('/hello')
def hello_word:
    return 'hello word'
```

- use methods
```python
app.add_url_rules('/hello', view_func=hello_world)
```

### parameters in `run`
- `host`: IP address: use mask '0.0.0.0', means can be accessed by computer from out web
- `debug`: `boolean`, set debug/production mode
- `port`


### config flle
- can import as a model
- use `app.config.from_object()`, accept the path of the config module
> app.config is the subclass of dict, so it can be retrieved as a dictionary


### view function
- status code: 200, 404, 301
- content-type: =text/html http headers, how to parser the returned text
- return a `Response` object
- `make_response` to create

#### requests v.s. urllib
- requests
    - `requests.get(url)`
- urllib
    - complicate

#### static method
- `@staticmethod` decorator
- python3: no different between `class CLS(Object):` and `class CLS:`


    