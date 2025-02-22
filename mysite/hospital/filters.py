from django_filters import FilterSet, ChoiceFilter
from .models import Doctor


class DoctorFilter(FilterSet):
    working_days = ChoiceFilter(choices=Doctor.WORKING_DAYS_CHOICES, field_name='working_days', lookup_expr='icontains')

    class Meta:
        model = Doctor
        fields = {
            'specialty': ['exact'],
            'department': ['exact'],
            'working_days': ['exact'],
            'service_price': ['gt', 'lt']
        }
