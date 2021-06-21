import os
import tornado.httpclient
import tornado.httpserver
import tornado.wsgi

from IPython.core.display import HTML


class Document:
    def __init__(self):
        self.document = None
        self.port = None

    def setup(self, document, db_url=None):
        """Setup cowork.

        The `db_url` should be formatted as a database url like:

            'driver://username:password@host:port/database'

        For SQLite, there should be four slashes for an absolute path:

            'sqlite:////absolute/path/to/db.sqlite'

        When `db_url` is None (the default), the SQLite driver will be used
        with the current working directory path like:

            cwd = os.getcwd()
            name = f'cowork-{document}.sqlite'
            f'sqlite:///{os.path.join(cwd, name)}'

        """
        if db_url is None:
            cwd = os.getcwd()
            name = f'cowork-{document}.sqlite'
            db_url = f'sqlite:///{os.path.join(cwd, name)}'
        os.environ.setdefault('DATABASE_URL', db_url)
        from .wsgi import application

        self.document = document
        container = tornado.wsgi.WSGIContainer(application)
        http_server = tornado.httpserver.HTTPServer(container)
        http_server.listen(0)
        port = next(iter(http_server._sockets.values())).getsockname()[1]
        self.port = port
        tags = '''
            <style>
              .jp-Notebook {
                background: lightgray;
              }

              #rendered_cells {
                display: inherit !important;
                max-width: 960px;
                margin: 0 auto;
                padding: 96px;
                box-shadow: 0 0 4px 4px gray;
                background: white;
              }
            </style>
            <script src="https://unpkg.com/htmx.org@1.3.0"></script>
        '''
        return HTML(tags)

    async def comments(self, topic):
        # TODO topic
        http_client = tornado.httpclient.AsyncHTTPClient()
        # TODO will localhost work in prod?
        resp = await http_client.fetch(
            f'http://localhost:{self.port}/comments/'
        )
        text = resp.body.decode()
        return HTML(text)


document = Document()
setup = document.setup
comments = document.comments
