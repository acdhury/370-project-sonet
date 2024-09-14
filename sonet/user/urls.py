from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.log_in, name = 'login'),
    path('logout/', views.log_out, name='logout'),
    path('register/', views.register_user, name='register')
]


