"""
URL configuration for ambiental_base project.

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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include('userAPI.urls')),
    path('api/v1/app/', include('appSettings.urls')),
    path('api/v1/disaster/', include('disasterType.urls')),
    path('api/v1/prevention/', include('Prevention.urls')),
    path('api/v1/action/', include('Protocol.urls')),
    path('api/v1/emergency/', include('Contact.urls')),
    path('api/v1/shelter/', include('Shelter.urls')),
    path('api/v1/blog/', include('Publication.urls')),
]


