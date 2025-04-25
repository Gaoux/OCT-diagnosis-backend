from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer
from rest_framework.views import APIView
from django.db.models import Count

# Create Report View
# This view allows authenticated users to create a report.
class CreateReportView(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# User Report List View
# This view allows authenticated users to view their own reports.
class UserReportListView(generics.ListAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user).order_by('-created_at')
    
# This view allows authenticated users to view their own reports.
# It retrieves a specific report based on the provided UUID.
class ReportDetailView(generics.RetrieveAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)

# This view allows authenticated users to update their own reports.
class ReportUpdateView(generics.UpdateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)

# This view allows authenticated users to delete their own reports.
# It retrieves a specific report based on the provided UUID.
class ReportDeleteView(generics.DestroyAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)
    
# This view allows authenticated users to view a summary of their reports.
# It retrieves:
# - The total number of reports, 
# - The most common diagnostics, 
# - The average confidence level.
class ReportSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_reports = Report.objects.filter(user=request.user)
        summary = {
            'total_reports': user_reports.count(),
            'most_common_diagnostics': user_reports.values('predicted_diagnostic').annotate(count=Count('id')).order_by('-count')[:5],
        }
        return Response(summary)
