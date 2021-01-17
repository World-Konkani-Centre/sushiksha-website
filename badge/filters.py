import django_filters
from users.models import Reward
from django_filters import CharFilter


class RewardFilter(django_filters.FilterSet):
    awarded_by = CharFilter(field_name='awarded_by', lookup_expr='icontains')

    class Meta:
        model = Reward
        fields = ['user', 'badges', 'awarded_by']
