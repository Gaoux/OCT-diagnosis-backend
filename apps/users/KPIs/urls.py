from django.urls import path
from .views import AdminKPIsView, ErrorReportView, AdminErrorReportsView, ErrorLogsView

urlpatterns = [
    path('admin/kpis/', AdminKPIsView.as_view(), name='admin-kpis'),
    path('errors/report/', ErrorReportView.as_view(), name='report-error'),  # Ruta para reportar errores
    path('admin/errors/', AdminErrorReportsView.as_view(), name='admin-errors'),  # Ruta para ver errores reportados
     path('admin/errors/<int:pk>/', AdminErrorReportsView.as_view(), name='admin-error-detail'),  # Para un error específico
     path('error-logs/', ErrorLogsView.as_view(), name='error-logs'),
]