"""Django URLs"""

from django.conf.urls import include, url
from django.contrib import admin

# Django REST Framework Routers
# router = routers.DefaultRouter()
# router.register(r'games', GameViewSet)
from channels_simple_app.views.views_core import HomePage

urlpatterns = (
    url(r'^$', HomePage.as_view(), name="home"),
    #    url(r'^', include(router.urls)),
    # Admin Site:
    url(r'^admin/', include(admin.site.urls)),
)
