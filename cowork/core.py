import getpass
import os
import tornado.httpclient
import tornado.httpserver
import tornado.wsgi

from IPython.core.display import HTML
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode


class Document:
    def __init__(self):
        self.document = None
        self.port = None

    async def setup(self, author, document, db_url=None):
        """Setup cowork.

        The `db_url` should be formatted as a database url like:

            'driver://username:password@host:port/database'

        For SQLite, there should be four slashes for an absolute path:

            'sqlite:////absolute/path/to/db.sqlite3'

        When `db_url` is None (the default), the SQLite driver will be used
        with the current working directory path like:

            cwd = os.getcwd()
            name = f'cowork-{document}.sqlite3'
            f'sqlite:///{os.path.join(cwd, name)}'

        """
        if db_url is None:
            cwd = os.getcwd()
            name = f'cowork-{document}.sqlite3'
            db_url = f'sqlite:///{os.path.join(cwd, name)}'
        os.environ.setdefault('DATABASE_URL', db_url)
        from django.core import management
        from .wsgi import application

        with ThreadPoolExecutor(1) as executor:
            future = executor.submit(
                management.call_command,
                'migrate',
                verbosity=0,
            )
            future.result()
        self.author = author
        self.document = document
        container = tornado.wsgi.WSGIContainer(application)
        http_server = tornado.httpserver.HTTPServer(container)
        http_server.listen(0)
        port = next(iter(http_server._sockets.values())).getsockname()[1]
        self.port = port
        tags = """
            <script>
                window.__define = window.define;
                window.__require = window.require;
                window.define = undefined;
                window.require = undefined;
            </script>
            <script src="https://unpkg.com/htmx.org@1.4.1"></script>
            <script>
                window.define = window.__define;
                window.require = window.__require;
                window.__define = undefined;
                window.__require = undefined;
            </script>
        """
        return HTML(tags)

    async def register(self, username):
        http_client = tornado.httpclient.AsyncHTTPClient()
        password = getpass.getpass()
        kwargs = {
            'username': username,
            'password1': password,
            'password2': password,
        }
        resp = await http_client.fetch(
            f'http://localhost:{self.port}/register/',
            method='POST',
            body=urlencode(kwargs),
        )
        text = resp.body.decode()
        return text

    async def comments(self, topic):
        http_client = tornado.httpclient.AsyncHTTPClient()
        # TODO will localhost work in prod?
        url = f'http://localhost:{self.port}/{self.author}/{self.document}/{topic}/comments/'
        resp = await http_client.fetch(url)
        text = resp.body.decode()
        return HTML(text)


document = Document()
setup = document.setup
register = document.register
comments = document.comments
