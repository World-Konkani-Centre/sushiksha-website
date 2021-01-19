import django_filters
from users.models import Reward
from django.contrib.auth.models import User
from django_filters import CharFilter, ModelChoiceFilter
from django.db.models.functions import Lower


class RewardFilter(django_filters.FilterSet):
    awarded_by = CharFilter(field_name='awarded_by', lookup_expr='icontains')
    user = ModelChoiceFilter(queryset=User.objects.all().order_by(Lower('username')))

    class Meta:
        model = Reward
        fields = ['user', 'badges', 'awarded_by']
