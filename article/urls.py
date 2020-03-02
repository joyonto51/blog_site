from django.urls import path
from .views import *

urlpatterns = [
    path('add/', ArticleAddView.as_view(), name='article_add'),
    path('list/', ArticleListView.as_view(), name='articles'),
    path('details/<int:article_id>/', ArticleDetailsView.as_view(), name='article_details'),

    path('comment/add/', CommentAddAPIView.as_view(), name='comment_add'),
    path('comment/delete/', CommentDeleteAPIView.as_view(), name='comment_delete'),
    path('comment/update/', CommentUpdateAPIView.as_view(), name='comment_update'),
]