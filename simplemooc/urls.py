"""simplemooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from simplemooc.core import urls as core
from simplemooc.courses import urls as courses
from simplemooc.forum   import urls as forum
from simplemooc.accounts import urls as accounts
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
    url(r'^', include(core, namespace='core')),
    url(r'^conta/', include(accounts, namespace='accounts')),
    url(r'^cursos/', include(courses , namespace='courses')),
    url(r'^forum/', include(forum , namespace='forum')),
    url(r'^admin/', include(admin.site.urls)),
]


if settings.DEBUG:    
  
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
