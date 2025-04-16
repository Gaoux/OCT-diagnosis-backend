from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, UserProfileView, UserViewSet, UserViewSet, AdminRegistrationView, DashboardStatsView

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin/register/', AdminRegistrationView.as_view(), name='admin-register'),
    path('admin/dashboard-stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('', include(router.urls)),
]
