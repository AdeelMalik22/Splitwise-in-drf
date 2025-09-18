from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import GroupViewSet, UserGroupViewSet, ExpenseViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'usersgroup', UserGroupViewSet, basename='usersgroup'),
router.register(r'expense',ExpenseViewSet,basename='expense')

urlpatterns = [
    path('', include(router.urls)),
]