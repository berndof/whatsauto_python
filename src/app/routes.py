from . import views

def setup_routes(app):
    app.router.add_get('/login', views.login_form)
    app.router.add_post('/login', views.login)
    app.router.add_get('/', views.index)