from django.urls import path, include
from rest_framework.routers import DefaultRouter
# pyrefly: ignore [missing-import]
from .views import ExpenseViewSet, AppSettingsView

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'settings', AppSettingsView, basename='settings')

urlpatterns = [
    path('', include(router.urls)),
]
