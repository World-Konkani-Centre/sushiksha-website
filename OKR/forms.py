from django import forms
from .models import Objective, KR, Entry


class ObjectiveCreationForm(forms.ModelForm):
    class Meta:
        model = Objective
        fields = ['objective']
        labels = {
            "objective": "Objective"
        }


class KRCreationForm(forms.ModelForm):
    class Meta:
        model = KR
        fields = ['objective', 'key_result', 'hours']
        labels = {
            "objective": "Objective",
            "key_result": "Key Result",
            "hours": "Hours to spend"
        }


class EntryCreationForm(forms.ModelForm):
    update = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 2,
        'minlength': 20,
        'title': "Brief update",

    }))
    objective = forms.ModelChoiceField(queryset=Objective.objects.all())

    class Meta:
        model = Entry
        fields = ['date_time','objective', 'key_result', 'update', 'time_spent']
        labels = {
            "date_time": "Date",
            "key_result": "Key Result",
            "update": "Brief update",
            "time_spent": "Productive time spent",
            "objective": "Objective",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['key_result'].queryset = KR.objects.none()

        if 'objective' in self.data:
            try:
                objective_id = int(self.data.get('objective'))
                self.fields['key_result'].queryset = KR.objects.filter(objective_id=objective_id).order_by('key_result')
            except (ValueError,TypeError):
                pass
