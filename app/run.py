import os
from contextlib import contextmanager

from flask import Flask
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool

from films import blueprint as films_blueprint
from reviews import blueprint as reviews_blueprint


class PoolWrapper:
    """Exists to provide an acquire method for easy usage.

        pool = PoolWrapper(...)
        with pool.acquire() as conneciton:
            connection.execute(...)
    """

    def __init__(self, max_pool_size: int, *, dsn):
        self._pool = ThreadedConnectionPool(
            1, max_pool_size, dsn=dsn, cursor_factory=RealDictCursor,
        )

    @contextmanager
    def acquire(self):
        try:
            connection = self._pool.getconn()
            yield connection
        finally:
            self._pool.putconn(connection)


def create_app():
    app = Flask(__name__)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

    @app.before_first_request
    def create_db():
        dsn = 'host=0.0.0.0 port=5432 dbname=dvdrental user=dvdrental password=dvdrental'
        app.pool = PoolWrapper(20, dsn=dsn)  #os.environ['DB_DSN'])

    app.register_blueprint(films_blueprint)
    app.register_blueprint(reviews_blueprint)

    return app


if __name__ == '__main__':
    create_app().run()
