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
        fields = ['objective', 'key_result']
        labels = {
            "objective": "Objective",
            "key_result": "Key Result"
        }


class EntryCreationForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['date_time', 'objective', 'key_result', 'percentage', 'update', 'time_spent']
        labels = {
            "date_time": "Date",
            "objective": "Objective",
            "key_result": "Key Result",
            "percentage": "Percentage",
            "update": "Brief update",
            "time_spent": "productive time spent"
        }
