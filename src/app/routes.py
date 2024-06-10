from app import views


def routes(router):
    router.add_get('/', views.home)
    router.add_get('/login', views.login_form)
    router.add_post('/login', views.login)