from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response


class ServerErrorProxyMiddleware(BaseHTTPMiddleware):
    async def handle_error(self) -> Response:
        pass

    async def handle_500(self):
        return await self.handle_error()

    async def handle_exception(self, exc):
        return await self.handle_error()

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            response = await call_next(request)
        except Exception as e:
            response = self.handle_exception(e)
        else:
            if response.status_code == 500:
                response = self.handle_500()
        return response
