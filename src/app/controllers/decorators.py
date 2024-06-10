from aiohttp import web
from aiohttp_session import get_session


def login_required(func):
    async def wrapped(request, *args, **kwargs):
        session = await get_session(request)
        if not session.get("user"):
            return web.HTTPFound("/login")
        return await func(request, *args, **kwargs)

    return wrapped

def admin_page(func):
    async def wrapped(request, *args, **kwargs):
        session = await get_session(request)
        if not session.get("user") or not session["user"]["is_admin"]:
            return web.HTTPUnauthorized(text="Unauthorized")
        return await func(request, *args, **kwargs)

    return wrapped