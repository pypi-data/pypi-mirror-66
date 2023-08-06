from starlette.applications import Starlette
from starlette.exceptions import ExceptionMiddleware
from starlette.middleware import Middleware
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.types import ASGIApp


class ContextApp(Starlette):
    def build_middleware_stack(self, *args, **kwargs) -> ASGIApp:
        super(ContextApp, self).build_middleware_stack(*args, **kwargs)
