from django.urls import path
from . import views

app_name = 'message'
urlpatterns = [
    path('chat/<int:recipient_id>/', views.chat, name='chat'),
    path('messages/', views.message_list, name='message_list'),
]
