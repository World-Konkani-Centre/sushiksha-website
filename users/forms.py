from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Reward, Mentions


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'batch', 'phone', 'college', 'degree', 'branch',
                  'profession', 'address', 'guidance',
                  'linkedin', 'instagram', 'twitter',
                  'github', 'okr', 'facebook',
                  'image']
        labels = {
            "okr": "OKR"
        }


class RewardForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Describe why your are giving the badge',
        'rows': 5,
        'minlength': 125,
    }))
    badges = forms.Select(attrs={
        'class': 'form-control'
    }
    )

    class Meta:
        model = Reward
        fields = ['description', 'badges']


class BadgeForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Describe why your are giving the badge',
        'rows': 5,
        'minlength': 125,
    }))

    badges = forms.Select(attrs={
        'class': 'form-control'
    }
    )

    class Meta:
        model = Reward
        fields = ['user', 'description', 'badges']

    def __init__(self, *args, **kwargs):
        super(BadgeForm, self).__init__(*args, **kwargs)
        # for visible in self.visible_fields():
        #     if visible.html_name == 'user' or visible.html_name == 'badges':
        #         visible.field.widget.attrs['class'] = 'fstdropdown-select'


class MentionUpdateForm(forms.ModelForm):
    team = forms.Select(attrs={
        'class': 'form-control'
    })
    house = forms.Select(attrs={
        'class': 'form-control'
    })
    user = forms.Select(attrs={
        'class': 'form-control'
    })

    class Meta:
        model = Mentions
        fields = ['title', 'team', 'house', 'user', 'image']


class RangeRequestForm(forms.Form):
    beginning = forms.DateTimeField(label="Start Date Time")
    end = forms.DateTimeField(label="End Date Time")
