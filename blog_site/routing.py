import aprs
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

import chat.routing

# application = ProtocolTypeRouter({
#     # Empty for now (http->django views is added by default)
#     'websocket': AuthMiddlewareStack(
#             URLRouter(
#                 chat.routing.websocket_urlpatterns,
#             )
#         ),
# })

# from chat.consumer2 import CommentConsumer, ChatConsumer
from chat.consumer3 import ChatConsumer

application = ProtocolTypeRouter({

    # WebSocket chat handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^messenger/$", ChatConsumer),
            # url(r"^messenger/$", ChatConsumer),
            # url(r"^comment/$", CommentConsumer),
        ])
    ),

    # Using the third-party project frequensgi, which provides an APRS protocol
    "aprs": aprs,

})

