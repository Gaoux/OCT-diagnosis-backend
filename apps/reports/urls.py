from django.urls import path
from .views  import (
    CreateReportView, UserReportListView,
    ReportDetailView, ReportDeleteView,
    ReportUpdateView, ReportSummaryView
)

urlpatterns = [
    path('create/', CreateReportView.as_view(), name='create-report'),
    path('history/', UserReportListView.as_view(), name='user-report-history'), 
    path('<uuid:pk>/', ReportDetailView.as_view(), name='report-detail'),
    path('<uuid:pk>/delete/', ReportDeleteView.as_view(), name='report-delete'),
    path('<uuid:pk>/update/', ReportUpdateView.as_view(), name='report-update'),
    path('summary/', ReportSummaryView.as_view(), name='report-summary'),
]
