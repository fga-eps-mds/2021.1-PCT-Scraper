from django.urls import include, path
from rest_framework import routers

from documents import views


router = routers.DefaultRouter()
router.register(r'', views.DocumentViewSet, basename='DocumentViewSet')

urlpatterns = [
    path(r'', include(router.urls)),
]
