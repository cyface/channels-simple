"""Django URLs"""

from django.conf.urls import include, url
from django.contrib import admin

from channels_simple_app.views.views_core import HomePage

urlpatterns = (
    url(r'^$', HomePage.as_view(), name="home"),
    # Admin Site:
    url(r'^admin/', include(admin.site.urls)),
)
