import tornado.httpclient
import tornado.httpserver
import tornado.wsgi

from IPython.core.display import HTML

from .wsgi import application


class Document:
    def __init__(self):
        self.port = None

    def setup(self, db_url=None, style=None):
        # TODO db_url
        # TODO style
        container = tornado.wsgi.WSGIContainer(application)
        http_server = tornado.httpserver.HTTPServer(container)
        http_server.listen(0)
        port = next(iter(http_server._sockets.values())).getsockname()[1]
        self.port = port
        tags = """
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
        """
        return HTML(tags)

    async def comments(self, name):
        # TODO name
        http_client = tornado.httpclient.AsyncHTTPClient()
        # TODO will localhost work in prod?
        resp = await http_client.fetch(f'http://localhost:{self.port}/comments/')
        text = resp.body.decode()
        return HTML(text)


document = Document()
setup = document.setup
comments = document.comments
