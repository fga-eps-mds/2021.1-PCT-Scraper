from django.urls import include, path
from rest_framework import routers

from documents import views

app_name = 'documents'
router = routers.DefaultRouter()
router.register(r'documents', views.DocumentViewSet, basename="Documents")



urlpatterns = [
    path(r'export/', views.DocumentExportViewSet.as_view(), name='documents-export'),
]
