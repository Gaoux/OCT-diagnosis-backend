from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer
from rest_framework.views import APIView
from django.db.models import Count
from django.http import FileResponse, Http404
from .permissions import IsProfessionalUser

# Create Report View
# This view allows authenticated users to create a report.
class CreateReportView(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessionalUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# User Report List View
# This view allows authenticated users to view their own reports.
class UserReportListView(generics.ListAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
         if self.request.user.is_admin:
            return Report.objects.all().order_by('-created_at')
         else:
            return Report.objects.filter(user=self.request.user).order_by('-created_at')
    
# This view allows authenticated users to view their own reports.
# It retrieves a specific report based on the provided UUID.
class ReportDetailView(generics.RetrieveAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
         if self.request.user.is_admin:
            return Report.objects.all()
         else:
            return Report.objects.filter(user=self.request.user).order_by('-created_at')

# This view allows authenticated users to update their own reports.
class ReportUpdateView(generics.UpdateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessionalUser]

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)

# This view allows authenticated users to delete their own reports.
# It retrieves a specific report based on the provided UUID.
class ReportDeleteView(generics.DestroyAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Si el usuario es superusuario o administrador, puede acceder a todos los reportes
        if self.request.user.is_admin:
            return Report.objects.all()
        # Si no, solo puede acceder a sus propios reportes
        return Report.objects.filter(user=self.request.user)
    
# This view allows authenticated users to view a summary of their reports.
# It retrieves:
# - The total number of reports, 
# - The most common diagnostics, 
# - The average confidence level.
class ReportSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsProfessionalUser]

    def get(self, request):
        user_reports = Report.objects.filter(user=request.user)
        summary = {
            'total_reports': user_reports.count(),
            'most_common_diagnostics': user_reports.values('predicted_diagnostic').annotate(count=Count('id')).order_by('-count')[:5],
        }
        return Response(summary)


class SecureMediaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, report_id):
        try:
            # Si el usuario es superusuario o administrador, puede acceder a cualquier reporte
            if request.user.is_admin:
                report = Report.objects.get(id=report_id)
            else:
                # Si no, solo puede acceder a sus propios reportes
                report = Report.objects.get(id=report_id, user=request.user)

            image_path = report.image.image_file.path
        except Report.DoesNotExist:
            raise Http404("Not found or permission denied")
        except Exception:
            raise Http404("Image unavailable")

        return FileResponse(open(image_path, 'rb'))