from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from .api import VerificationViewSet, app

router = routers.DefaultRouter()
router.register(r"verification", VerificationViewSet, basename="verification")

urlpatterns = [
    url("api/", include(router.urls)),
    path("admin/", admin.site.urls),
    # React router paths
    path("", app, name="home"),
]
