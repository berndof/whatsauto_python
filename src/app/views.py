from aiohttp_session import get_session
from aiohttp import web
from app.controllers.decorators import login_required
from aiohttp_jinja2 import render_template_async
from app.modules.security import Security

#@login_required
@login_required
async def home(request):
    context = {}
    return await render_template_async("home.html", request,  context)

async def login_form(request):
    context = {}
    # example
    # data = await manager.get_data

    return await render_template_async("login.html", request, context)

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