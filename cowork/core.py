import tornado.httpclient
import tornado.httpserver
import tornado.wsgi

from IPython.core.display import HTML

from .wsgi import application


class Document:
    def __init__(self):
        self.port = None

    def setup(self):
        container = tornado.wsgi.WSGIContainer(application)
        http_server = tornado.httpserver.HTTPServer(container)
        http_server.listen(0)
        port = next(iter(http_server._sockets.values())).getsockname()[1]
        self.port = port
        script_tags = """
            <script src="https://unpkg.com/htmx.org@1.3.0"></script>
        """
        return HTML(script_tags)

    def style(self):
        css = """
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
        """
        return HTML(css)

    async def comments(self):
        http_client = tornado.httpclient.AsyncHTTPClient()
        resp = await http_client.fetch(f'http://localhost:{self.port}/comments/')
        text = resp.body.decode()
        return HTML(text)


document = Document()
setup = document.setup
style = document.style
comments = document.comments
