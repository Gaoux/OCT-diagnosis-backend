from rest_framework import serializers
from .models import ErrorReport

class AdminKPIsSerializer(serializers.Serializer):
    users_last_30_days = serializers.IntegerField()
    active_users_last_month = serializers.IntegerField()
    average_logins_per_user = serializers.FloatField()
    role_distribution = serializers.ListField(
        child=serializers.DictField()
    )

class ErrorReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorReport
        fields = ['id', 'user', 'description', 'created_at', 'resolved']
        read_only_fields = ['id','user','created_at']