import cherrypy
import os
import sys
import logging
import logging.config
from .logging import AccessLogColorFormatter


class WebApp(object):
    def __init__(self, app_class):
        self._config = {}
        self._setup_app(app_class)
        self._application = cherrypy.tree.mount(self._app)
        self._setup_logging()

    def _setup_logging(self):
        # setup color logging only when running from terminal
        if sys.stdin.isatty():
            log = self._application.log

            log.access_file = None  # Remove default log handler
            h = logging.StreamHandler()
            h.setFormatter(AccessLogColorFormatter(log.access_log_format))
            log.access_log.addHandler(h)
            log.access_log.propagate = False

    def _setup_app(self, app_class):
        app = self._app = app_class()
        object_methods = [
            method_name
            for method_name in dir(app)
            if method_name[0] != "_" and callable(getattr(app, method_name))
        ]
        for method_name in object_methods:
            class_method = getattr(app_class, method_name)
            setattr(class_method, "exposed", True)

    def run(self):
        server_software = os.environ.get("SERVER_SOFTWARE")
        if server_software:
            return cherrypy.Application(self._app, "/")
        else:
            # In some platforms signals are not available
            if hasattr(cherrypy.engine, "signals"):
                cherrypy.engine.signals.subscribe()
            cherrypy.engine.start()
            cherrypy.engine.block()
