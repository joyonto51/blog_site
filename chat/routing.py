# from django.urls import re_path, path
#
# from . import consumers, consumer2
#
# websocket_urlpatterns = [
#     # re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
#     re_path(r'ws/chat/(?P<room_name>\w+)/$', consumer2.ChatConsumer),
#     # path(r'ws/chat/<str:room_name>/$', consumers.ChatConsumer),
# ]