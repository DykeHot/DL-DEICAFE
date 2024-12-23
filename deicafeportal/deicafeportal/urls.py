"""
URL configuration for deicafeportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from deicafeapp import views
from django.conf import settings
from django.conf.urls.static import static

c = "customer/"
d = "debug/"

#app_name = "customera"

urlpatterns = [
    path('admin/', admin.site.urls),
    #顧客用画面
    path("", views.deicafebasis.as_view(), name = "basis"),
    #path(c, include("customera.urls")),
    path(c + "login/", views.login.as_view(), name = "login"),
    path(c + "top/", views.top.as_view(), name = "top"),
    path(c + "createaccount/", views.createaccount.as_view(), name = "creteaccount"),
    path(c + "reservation/", views.reservationlog.as_view(), name="reservation"),
    path(c + "logout/", views.logout.as_view(), name = "logout"),
    #店舗用画面
    path("db/", views.deicafebasis.as_view(), name = "debugbasis"),
    path(d + "debuglogin/", views.debuglogin.as_view(), name = "debuglogin"),
    path(d + "top/", views.debugtop.as_view(), name = "debugtop"),
    path(d + "logoutsuccess/", views.debuglogout.as_view(), name = "debuglogout"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)