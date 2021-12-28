# -*- coding: utf-8 -*-
"""autoproject URL Configuration

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
import sys

from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import path

from backend.autoproject import settings

sys.path.append('../')

from backend.api.v1 import v1

urlpatterns = [
    # path('admin/', admin.site.urls),

    # Ninja-API
    path('v1/', v1.urls),

    path(r'static/<path:path>', serve, {'document_root': settings.STATIC_ROOT, }, ),
    path(r'media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}, ),
]
