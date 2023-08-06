# Loquat

A simple web framework based on Tornado.

## Introduce

Loquat is a web framework based on Tornado.

## Installation

```shell
pip install loquat
```

## Simple uses

```python
from loquat.server import Server
from loquat.web import Application

from handler import BaseHandler


class IndexHandler(BaseHandler):
    def initialize(self, database):
        self.database = database

    def get(self):
        self.write("hello world!")


class TestApplication(Application):
    def __init__(self, handlers=None, middlewares=None, transforms=None):
        super().__init__(handlers, middlewares, transforms)


def main():
    handlers = [
        (r"/", IndexHandler, dict(database="this is database"))
    ]
    application = TestApplication(handlers=handlers)
    server = Server(application)
    server.start()

if __name__ == "__main__":
    main()

```