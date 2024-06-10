
from app import routes

class routeController:
    def __init__(self, app):
        self.app = app
        routes.routes(self.app.router)