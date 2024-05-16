from lato import Application
from starlette.requests import Request


async def get_application(request: Request) -> Application:
    application = request.app.extra["container"].application()
    return application
