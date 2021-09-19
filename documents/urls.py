from django.urls import include, path
from rest_framework import routers

from documents.views.informacao_views import InformacaoViewSet
from documents.views.glossario_views import GlossarioViewSet


router = routers.DefaultRouter()
router.register(r'informacao', InformacaoViewSet)
router.register(r'glossario', GlossarioViewSet)

urlpatterns = [
  path(r'', include(router.urls)),
]