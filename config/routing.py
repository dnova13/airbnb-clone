from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from conversations import routing as conv_routing
from core import routing as core_routing


# View에 해당하는 Consumer로 연결될 라우팅(django의 url에 해당함)을 해주는 부분
application = ProtocolTypeRouter(
    {
        # AuthMiddlewareStack으로 연결 되는데,
        # 해당 미들웨어는 장고의 AuthenticationMiddleware와 비슷하게,
        # 인증된 유저여부에 따라서 연결의 scope 를 제한하게 된다.
        # scope 는 일종의 Django의 세션과 비슷한거라고 보면 된다.
        "websocket": AuthMiddlewareStack(
            #  실제 URLRouter에서 넘겨받은 URL을 기반으로 그에 맞는 핸들러를 실행
            URLRouter(
                conv_routing.websocket_urlpatterns + core_routing.websocket_urlpatterns
            ),
        ),
    }
)

ASGI_APPLICATION = "config.routing.application"
