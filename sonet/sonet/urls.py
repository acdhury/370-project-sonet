"""
URL configuration for sonet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('feed/', include('feed.urls')),  # Feed app URLs
    path('follow/', include('follow.urls')),  # Follow app URLs
    path('message/', include('message.urls')),  # Message app URLs
    path('post/', include('post.urls')),  # Post app URLs
    path('user/', include('user.urls')),  # User app URLs
    path('user/', include('django.contrib.auth.urls')),  # Django Auth URLs
    path('profile/', include('account.urls')),  # Account/profile URLs
    path('search/', include('search.urls')),  # Search app URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
