import tornado.web

from .exception import ArgumentError
from .middleware import MiddlewareManager, MiddlewareType
from .config import load_config_dir


class Application(tornado.web.Application):
    """Loquat Application"""

    def __init__(self, handlers=None, transforms=None):

        config = load_config_dir()
        default_host = config['default_host']
        app_settings = config['app_settings']

        self._init_middleware(config)

        super(Application, self).__init__(handlers=handlers, default_host=default_host, transforms=transforms,
                                          **app_settings)

    def _init_middleware(self, config):

        default_middlewares = ['middleware.MixinHandlerMiddleware']

        if not isinstance(config['middleware_classes'], list):
            raise ArgumentError('middleware_classes must be list')

        self.middleware_manager = MiddlewareManager()
        self.middleware_manager.register_all(config['middleware_classes'] + default_middlewares)
        self.middleware_manager.run_middleware_type(MiddlewareType.INIT_APPLICATION, self)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)
