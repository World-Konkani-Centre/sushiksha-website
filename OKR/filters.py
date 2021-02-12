import django_filters
from .models import Objective, KR, Entry
# from django_filters import CharFilter, ModelChoiceFilter
from django.db.models.functions import Lower


class ObjectiveKRFilter(django_filters.FilterSet):
    class Meta:
        model = Entry
        fields = ['key_result', 'key_result__objective']
