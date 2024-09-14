from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('<int:post_id>/like/', views.like_post, name='like_post'),
    path('<int:post_id>/comment/', views.comment_on_post, name='comment_on_post'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
]
