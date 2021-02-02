from django import forms


class UrlRequestForm(forms.Form):
    URL = forms.URLField(label="cuckoo url")
