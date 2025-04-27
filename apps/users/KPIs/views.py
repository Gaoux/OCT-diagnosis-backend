from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import ErrorReport
from .serializers import ErrorReportSerializer
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Avg, Count
from ..models import UserAccount  

from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        # Verifica que el usuario esté autenticado y sea administrador
        return request.user and request.user.is_authenticated and request.user.is_admin

class AdminKPIsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        last_30_days = now() - timedelta(days=30)

        # Calcular KPIs
        users_last_30_days = UserAccount.objects.filter(date_joined__gte=last_30_days).count()
        active_users_last_month = UserAccount.objects.filter(last_login__gte=last_30_days).count()
        average_logins_per_user = UserAccount.objects.aggregate(avg_logins=Avg('login_count'))['avg_logins'] or 0
        role_distribution = UserAccount.objects.values('role').annotate(count=Count('role'))

        # KPI de errores reportados
        total_errors_reported = ErrorReport.objects.count()
        unresolved_errors = ErrorReport.objects.filter(resolved=False).count()

        # KPIs finales
        kpis = {
            'users_last_30_days': users_last_30_days,
            'active_users_last_month': active_users_last_month,
            'average_logins_per_user': average_logins_per_user,
            'role_distribution': role_distribution,
            'total_errors_reported': total_errors_reported,
            'unresolved_errors': unresolved_errors,
        }

        return Response(kpis)

class ErrorReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Permite a los usuarios reportar un error."""
        serializer = ErrorReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class AdminErrorReportsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk=None):
        """Devuelve los detalles de un error específico o una lista de todos los errores."""
        if pk:
            # Detalles de un error específico
            try:
                error_report = ErrorReport.objects.get(pk=pk)
                serializer = ErrorReportSerializer(error_report)
                return Response(serializer.data)
            except ErrorReport.DoesNotExist:
                return Response({'error': 'Error reportado no encontrado'}, status=404)
        else:
            # Lista de todos los errores con soporte para filtros
            resolved = request.query_params.get('resolved')
            if resolved is not None:
                # Convertir el valor del parámetro a booleano
                resolved = resolved.lower() == 'true'
                error_reports = ErrorReport.objects.filter(resolved=resolved)
            else:
                error_reports = ErrorReport.objects.all()

            serializer = ErrorReportSerializer(error_reports, many=True)
            return Response(serializer.data)

    def patch(self, request, pk=None):
        """Actualiza parcialmente un error reportado."""
        if not pk:
            return Response({'error': 'Se requiere un ID para actualizar un error'}, status=400)

        try:
            error_report = ErrorReport.objects.get(pk=pk)
        except ErrorReport.DoesNotExist:
            return Response({'error': 'Error reportado no encontrado'}, status=404)

        serializer = ErrorReportSerializer(error_report, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)