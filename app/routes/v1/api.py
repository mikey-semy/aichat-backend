from app.routes.base import BaseRouter

# from app.routes.v1.auth import AuthRouter
# from app.routes.v1.register import RegisterRouter
from app.routes.v1.chat import ChatRouter

class APIv1(BaseRouter):
    def configure_routes(self):
        # Создаем и подключаем роутеры
        self.router.include_router(ChatRouter().get_router())
        # self.router.include_router(AuthRouter().get_router())
        # self.router.include_router(RegisterRouter().get_router())
