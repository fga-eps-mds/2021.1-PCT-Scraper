from django.urls import include, path
from rest_framework import routers

from documents import views


router = routers.DefaultRouter()
# router.register(r'glossary', views.GlossaryViewSet)

urlpatterns = [
    path("", views.DocumentViewSet.as_view()),
]
