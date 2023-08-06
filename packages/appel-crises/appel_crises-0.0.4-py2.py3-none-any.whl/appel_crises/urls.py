"""appel_crises URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path

from appel_crises.api import sign, search_depute
from appel_crises.views import home, success, form_no_js

urlpatterns = [
    path('admin/', admin.site.urls),
    path('success', success, name='success'),
    path('api/sign', sign, name='sign'),
    path('api/search-depute', search_depute, name='search-depute'),
    path('', home),
    path('form', form_no_js, name="form-no-js"),
]
