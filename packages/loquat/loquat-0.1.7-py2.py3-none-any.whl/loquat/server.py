import logging
import signal
import time

import tornado.escape
import tornado.ioloop
import tornado.locks
import tornado.web
from tornado.options import options

from .log import initialize_logging, NullHandler
from .config import load_config_dir
from .web import Application

# 这里是为了Tornado不初始化日志
logging.getLogger().addHandler(NullHandler())
logger = logging.getLogger(__name__)


def define_server_options():
    """options.define定制"""

    options.define('profile', default='', help='', type=str)
    options.define('config_dir', default='', help='', type=str)


define_server_options()
options.parse_command_line()


class Server(object):
    def __init__(self, application: Application = None, ioloop: object = None, **kwargs):
        """
        @param application: loquat.web.Application及其子类
        @param ioloop: An I/O event loop.
        @param kwargs: 可变参数，可选参数有：
            - config: 配置
            - config_dir： 配置的目录
        """
        self.application = application
        self.ioloop = ioloop
        self.http_server = None

        self._set_config(**kwargs)
        initialize_logging(options=self.config['log'])

    def _set_config(self, **kwargs):
        """设置服务配置

        配置优先级：
            1- 系统运行时传入的配置文件
            2- Server初始化时候的配置
            3- 默认的配置文件
        """

        if kwargs:
            if 'config' in kwargs.keys():
                self.config = kwargs['config']

        # 初始化配置
        config_dir = ''
        if 'config_dir' in kwargs.keys():
            config_dir = kwargs['config_dir']
        if options.config_dir:  # 如果存在 options.config_dir
            config_dir = options.config_dir
        self.config = load_config_dir(config_dir, options.profile)

    def start(self):
        """开始服务"""

        if not self.application:
            app_settings = self.config['app_settings']
            self.application = Application(**app_settings)

        if not self.http_server:
            self.http_server = tornado.httpserver.HTTPServer(self.application, xheaders=True)
        self.http_server.listen(self.config['port'])

        # 处理系统信号
        signal.signal(signal.SIGTERM, self.shutdown_signal_handler)
        signal.signal(signal.SIGINT, self.shutdown_signal_handler)

        logger.info("Application started on port %s." % (self.config['port'],))

        if not self.ioloop:
            self.ioloop = tornado.ioloop.IOLoop.instance()
        self.ioloop.start()

    def shutdown_signal_handler(self, sig, frame):
        """handle shutdown signal"""

        logger.warning('caught signal: %s', sig)

        max_wait_seconds_before_shutdown = 1

        def shutdown():
            logger.info('stopping http server')
            self.http_server.stop()

            logger.info('will shutdown in %s seconds...', max_wait_seconds_before_shutdown)

            deadline = time.time() + max_wait_seconds_before_shutdown

            def stop_loop():
                now = time.time()
                if now < deadline:
                    self.ioloop.add_timeout(now + 1, stop_loop)
                else:
                    logger.info('shutdown')
                    self.ioloop.stop()

            stop_loop()

        self.ioloop.add_callback(shutdown)


def server_start(application: Application):
    server = Server(application)
    server.start()
