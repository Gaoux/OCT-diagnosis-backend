from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, UserProfileView, AdminUserUpdateView, UserViewSet, UserViewSet,AdminRegistrationView, DashboardStatsView,RecentUsersView, VerifyEmailView, ForgotPasswordView, ResetPasswordView

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', AdminRegistrationView.as_view(), name='admin-register'),
    path('admin/dashboard-stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('kpis/', include('apps.users.KPIs.urls')),  
    path('admin/recent-users/', RecentUsersView.as_view(), name='recent-users'),
    path('', include(router.urls)),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('admin/users/<uuid:pk>/update/', AdminUserUpdateView.as_view(), name='admin-user-update')

]
