from django.urls import include, path
from rest_framework import routers

from documents import views


router = routers.DefaultRouter()
router.register(r'documents', views.DocumentViewSet)
router.register(r'glossary', views.GlossaryViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path("api/documents/", views.DocumentByKeyWordViewSet.as_view()),
]
