import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session

def login_required(func):
    async def wrapped(request, *args, **kwargs):
        session = await get_session(request)
        if not session.get("user"):
            return web.HTTPFound("/login")
        return await func(request, *args, **kwargs)

    return wrapped

async def login_form(request):
    context = {}
    # example
    # data = await manager.get_data

    return await aiohttp_jinja2.render_template_async("login.html", request, context)

async def login(request):
    # Pega os dados do formulário de login
    data = await request.post()
    username = data.get("username")
    password = data.get("password")

    manager = request.app["manager"]
    user = await manager.security.authenticate(username, password)
    if user:

        session = await get_session(request, max_age=3600)
        session["user"] = str({"id": user.id, "is_admin": user.is_admin, "username": user.username, "queuesUnderSupervision": user.queuesUnderSupervision})
        return web.HTTPFound('/')  # Redirecione o usuário para a página inicial após o login

    else:
       return web.HTTPUnauthorized(text="Credenciais inválidas")

@login_required
async def index(request):

    return await aiohttp_jinja2.render_template_async("index.html", request, {})