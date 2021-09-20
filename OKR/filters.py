import django_filters
from .models import Entry, Objective, KR
from django_filters import ModelChoiceFilter
from django.contrib.auth.models import User
from django.db.models.functions import Lower


class OKRFilter(django_filters.FilterSet):
    user = ModelChoiceFilter(queryset=User.objects.all().order_by(Lower('username')))

    class Meta:
        model = Entry
        fields = ['user']

class ObjectiveKRFilter(django_filters.FilterSet):
    key_result__objective = django_filters.filters.ChoiceField(label='Objective')

    class Meta:
        model = Entry
        fields = ['key_result__objective', 'key_result']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ObjectiveKRFilter, self).__init__(*args, **kwargs)
        self.filters['key_result__objective'].label = "Objective"
        self.filters['key_result__objective'].queryset = Objective.objects.filter(user=user)
        self.filters['key_result'].queryset = KR.objects.filter(objective__user=user)