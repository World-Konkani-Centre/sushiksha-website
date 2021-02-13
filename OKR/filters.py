import django_filters

from .models import Entry


# from django_filters import CharFilter, ModelChoiceFilter


class ObjectiveKRFilter(django_filters.FilterSet):
    class Meta:
        model = Entry
        fields = ['key_result', 'key_result__objective']
