# -*- coding: utf-8 -*-
"""ninja_xia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.staticfiles.views import serve
from django.urls import path

from backend.api import register_app
from backend.ninja_xia import settings

urlpatterns = [
    # path('admin/', admin.site.urls),

    # Ninja-API
    path('v1/', register_app().urls),

    path(r'static/<path:path>', serve, {'document_root': settings.STATIC_ROOT, }, ),
    path(r'media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}, ),
]
