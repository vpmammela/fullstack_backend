from starlette.responses import Response


class AuthResponseHandlerBase:
    async def send(self, res: Response, access: str, refresh: str, csrf: str, sub: str):
        pass