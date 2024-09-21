from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('update_name/', views.update_name, name='update_name'),  
    path('update-bio/', views.update_bio, name='update_bio'),
    path('update-profile-picture/', views.update_profile_picture, name='update_profile_picture'), 
]
