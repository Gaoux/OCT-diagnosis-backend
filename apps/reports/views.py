from rest_framework import generics, permissions
from .models import Report
from .serializers import ReportSerializer

class CreateReportView(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
