"""wisfinitv0 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings #add this
from django.conf.urls.static import static #add this

from django.contrib import admin
from django.urls import path
from homepage.views import home_screen_view
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from registration.views import signup_view
from registration.views import getstarted
from registration.views import signin
from user.views import user
from user.views import dashboard

from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('home/', home_screen_view, name='home'),
                  path('', home_screen_view, name='home'),
                  path('signup/', signup_view, name='signup'),
                  path('signup/getstarted/', getstarted, name='getstarted'),
                  path('signin/', signin, name='signin'),
                  path('dashboard/', dashboard, name='dashboard'),
                  path('user/', user, name='user'),
                  path('cookies/', include('cookie_consent.urls'))

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
