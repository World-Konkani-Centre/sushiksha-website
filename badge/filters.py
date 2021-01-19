import django_filters
from users.models import Reward, User
from django_filters import CharFilter, ModelChoiceFilter


class RewardFilter(django_filters.FilterSet):
    awarded_by = CharFilter(field_name='awarded_by', lookup_expr='icontains')
    user = ModelChoiceFilter(queryset=User.objects.all().order_by('username'))

    class Meta:
        model = Reward
        fields = ['user', 'badges', 'awarded_by']
