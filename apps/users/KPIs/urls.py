from django.urls import path
from .views import AdminKPIsView,AdminReportsView

urlpatterns = [
    path('admin/kpis/', AdminKPIsView.as_view(), name='admin-kpis'),
    path('admin/errors/', AdminReportsView.as_view(), name='admin-errors'), 
]