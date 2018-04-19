from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import logout
from django.contrib.auth.views import login
from django.views.static import serve
from myproject import settings

urlpatterns = [

    url(r'^logout$', logout),
    url(r'^login', login),
    url(r'^anotated$','cms.views.home_anotated'), #me lleva a la pagina PRINCIPAL con plantilla
    url(r'^edit/(\w+)$','cms.views.edit'),
    url(r'^$','cms.views.home'), #me lleva a la pagina PRINCIPAL
    url(r'^(\w+)$','cms.views.pagina'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<path>.*)$', serve, {'document_root': settings.STATIC_URL})

]
