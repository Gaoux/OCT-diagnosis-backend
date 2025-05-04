import django_filters
from .models import UserAccount

class UserFilter(django_filters.FilterSet):
    role = django_filters.CharFilter(field_name='role', lookup_expr='exact')  # Filtro para el campo 'role'

    class Meta:
        model = UserAccount
        fields = ['role']  # Solo se filtra por 'role'