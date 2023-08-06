import inspect
import logging
from abc import ABCMeta, abstractmethod

from .exception import ArgumentError
from .util import import_object

logger = logging.getLogger(__name__)


class MiddlewareType:
    INIT_APPLICATION = 'INIT_APPLICATION'  # 在application的init时候调用
    BEFORE_REQUEST = 'BEFORE_REQUEST'  # 在request之前
    AFTER_RESPONSE = 'AFTER_RESPONSE'  # 在response之后
    HANDLE_FINISHED = 'HANDLE_FINISHED'  # 在请求结束之后
    dict = {
        INIT_APPLICATION: "INIT_APPLICATION",
        BEFORE_REQUEST: "BEFORE_REQUEST",
        AFTER_RESPONSE: "AFTER_RESPONSE",
        HANDLE_FINISHED: "HANDLE_FINISHED"
    }


class BaseMiddleware(metaclass=ABCMeta):

    def __init__(self, mw_order=0, mw_type=MiddlewareType.BEFORE_REQUEST):

        self._mw_order = mw_order
        self._mw_type = mw_type

    @property
    def mw_order(self):
        """middleware的执行顺序，值越小越靠前执行
        """
        return self._mw_order

    @mw_order.setter
    def mw_order(self, value):
        if not isinstance(value, int):
            raise ValueError('value must be an integer!')
        if value < 0:
            raise ValueError('value must bigger than 0!')
        self._mw_order = value

    @property
    def mw_type(self):
        """middleware的类型。有：MiddlewareType.FINISHED, MiddlewareType.AFTER_RESPONSE, MiddlewareType.BEFORE_REQUEST
        """
        return self._mw_type

    @mw_type.setter
    def mw_type(self, value):

        if value not in [MiddlewareType.HANDLE_FINISHED, MiddlewareType.AFTER_RESPONSE, MiddlewareType.BEFORE_REQUEST]:
            raise ValueError(
                'value must in [MiddlewareType.FINISHED, MiddlewareType.AFTER_RESPONSE, MiddlewareType.BEFORE_REQUEST]')

        self._mw_type = value

    @abstractmethod
    def should_run(self, component, *args, **kwargs) -> bool:
        """
        是否需要运行中间件。True为运行，False为不运行
        @param component: tornado.web.RequestHandler的子类 或者其他
        @param args:
        @param kwargs:
        """
        pass

    @abstractmethod
    def run(self, component, *args, **kwargs) -> None:
        """
        运行中间件
        @param component: tornado.web.RequestHandler的子类 或者其他
        @param args:
        @param kwargs:
        """
        pass


# class SingletonMiddlewareManagerType(type):
#     _instance_lock = threading.Lock()
#
#     def __call__(cls, *args, **kwargs):
#         if not hasattr(cls, "_middleware_manager"):
#             with SingletonMiddlewareManagerType._instance_lock:
#                 if not hasattr(cls, "_middleware_manager"):
#                     cls._middleware_manager = super(SingletonMiddlewareManagerType, cls).__call__(*args, **kwargs)
#         return cls._middleware_manager


class MiddlewareManager(object):

    def __init__(self) -> None:
        self.init_application_list = []
        self.before_request_list = []
        self.after_response_list = []
        self.handle_finished_list = []

    def register(self, middleware):
        """注册中间件"""
        if not middleware:
            return
        if isinstance(middleware, str):
            middleware = import_object(middleware)
        if not issubclass(middleware, BaseMiddleware):
            cl = [c for c in inspect.getmro(middleware) if c.__name__ == 'BaseMiddleware']
            if len(cl) < 1:
                raise ArgumentError("middleware must be a subclass of BaseMiddleware")

        instance = middleware()
        mw_type = instance.mw_type
        if mw_type is MiddlewareType.INIT_APPLICATION:
            self.init_application_list.append(instance)
            self.init_application_list = sorted(self.init_application_list, key=lambda m: m.mw_order)
        elif mw_type is MiddlewareType.BEFORE_REQUEST:
            self.before_request_list.append(instance)
            self.before_request_list = sorted(self.before_request_list, key=lambda m: m.mw_order)
        elif mw_type is MiddlewareType.AFTER_RESPONSE:
            self.after_response_list.append(instance)
            self.after_response_list = sorted(self.after_response_list, key=lambda m: m.mw_order)
        elif mw_type is MiddlewareType.HANDLE_FINISHED:
            self.handle_finished_list.append(instance)
            self.handle_finished_list = sorted(self.handle_finished_list, key=lambda m: m.mw_order)

    def register_all(self, middlewares):
        """注册多个中间件"""
        if not middlewares:
            return

        for middleware in middlewares:
            self.register(middleware)

    def run_middleware_type(self, mw_type: str, component: object, *args, **kwargs) -> tuple:
        """
        根据中间件的类型运行中间件列表
        @param mw_type:
        @param component:
        @param args:
        @param kwargs:
        @return:
        """
        mws = []
        if mw_type is MiddlewareType.INIT_APPLICATION:
            mws = self.init_application_list
        elif mw_type is MiddlewareType.BEFORE_REQUEST:
            mws = self.before_request_list
        elif mw_type is MiddlewareType.AFTER_RESPONSE:
            mws = self.after_response_list
        elif mw_type is MiddlewareType.HANDLE_FINISHED:
            mws = self.handle_finished_list

        res_list = []
        for m in mws:
            res = self.run_middleware(m, component, *args, **kwargs)
            res_list.append(res)
        return tuple(res_list)

    def run_middleware(self, middleware, component, *args, **kwargs):
        """
        运行中间件
        @param middleware:
        @param component:
        @param args:
        @param kwargs:
        @return:
        """
        try:
            should_run_res = middleware.should_run(component, *args, **kwargs)
            if should_run_res:
                res = middleware.run(component, *args, **kwargs)
                return res
        except Exception as e:
            logger.exception(e)
            raise e


# 以下为系统默认的中间件
class MixinHandlerMiddleware(BaseMiddleware):
    """
    组合Handler的中间件。根据application进行判断是否要组合
    """

    def __init__(self, mw_order=0, mw_type=MiddlewareType.INIT_APPLICATION):
        super().__init__(mw_order, mw_type)

        self.mm_should = False  # 是否组合MiddlewareHandlerMixin

    def should_run(self, application, *args, **kwargs) -> bool:
        m = application.middleware_manager
        # 如果存在中间件，那么就设置为true
        mm_should = len(m.before_request_list) > 0 or len(m.after_response_list) > 0 or len(m.handle_finished_list) > 0
        self.mm_should = mm_should
        return self.mm_should

    def run(self, application, *args, **kwargs) -> None:
        if self.mm_should:
            from handler import BaseHandler, MiddlewareHandlerMixin
            # 一定要将BaseHandler.__bases__ 写后面，这样才能覆盖，使用MiddlewareHandlerMixin中的方法
            BaseHandler.__bases__ = (MiddlewareHandlerMixin,) + BaseHandler.__bases__
