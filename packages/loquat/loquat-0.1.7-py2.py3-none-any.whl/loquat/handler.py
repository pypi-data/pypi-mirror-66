import logging
from typing import Optional, Awaitable, Any, Union

import tornado.web
from tornado import httputil

from .middleware import MiddlewareType

logger = logging.getLogger(__name__)


class MiddlewareHandlerMixin(object):
    def __init__(self, application, request, **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)

        self.middleware_manager = self.application.middleware_manager

    def prepare(self) -> Optional[Awaitable[None]]:
        """
        在每个请求的最开始的时候被调用, 在 get/post/等方法之前.
        """
        super().prepare()
        return self._process_middlewares(mw_type=MiddlewareType.BEFORE_REQUEST)

    def on_finish(self) -> None:
        """在一个请求结束后被调用."""
        super().on_finish()
        self._process_middlewares(mw_type=MiddlewareType.HANDLE_FINISHED)

    def finish(self, chunk: Union[str, bytes, dict] = None) -> "Future[None]":
        """完成响应后调用."""
        # finish之前可能执行过多次write，反而chunk可能为None
        # 真正的chunk数据在self._write_buffer中，包含历次write的数据
        # 这里将chunk数据write进_write_buffer中，然后将chunk置空
        if chunk:
            self.write(chunk)
            chunk = None
        self._process_middlewares(MiddlewareType.AFTER_RESPONSE, chunk)
        return super().finish(chunk)

    def _process_middlewares(self, mw_type, *args, **kwargs):
        """根据中间件类型执行中间件"""
        self.middleware_manager.run_middleware_type(mw_type, self, *args, **kwargs)


class _PatchHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs) -> None:
        super().__init__(application, request, **kwargs)

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass


class BaseHandler(_PatchHandler):
    """A class to collect common handler methods - all other handlers should subclass this one.
    """

    def __init__(self, application: "Application", request: httputil.HTTPServerRequest, **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)


class RestfulHandler(BaseHandler):
    def __init__(self, application, request, **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
