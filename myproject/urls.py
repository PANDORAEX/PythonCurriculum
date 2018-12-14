"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.conf.urls import include, url
from login import views
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.login, name="direct_login"),
    url(r'^admin/', admin.site.urls, name="admin.site"),
    url(r'^index/', views.index, name="views.index"),
    url(r'^login/', views.login, name="views.login"),
    url(r'^add/', views.add, name="views.add"),
    url(r'^list/', views.list_req, name="views.list"),
    url(r'^edit/(?P<project_id>\d+)/$', views.edit, name='edit'),
    url(r'^delete/(?P<project_id>\d+)/$', views.delete, name='delete'),
    url(r'^emotion/', views.emotion, name="views.emotion"),
]
