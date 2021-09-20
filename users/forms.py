from django import forms
import django
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models.functions import Lower
from .models import Profile, Reward, Mentions, Badge
from django.contrib.auth.models import User



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
                  'profession', 'address', 'guidance', 'slack_id',
                                                       'linkedin', 'instagram', 'twitter',
                  'github', 'okr', 'facebook',
                  'image']
        labels = {
            "okr": "OKR",
            'slack_id': "Slack Id"
        }


class RewardForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Describe why you are giving the badge',
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
        'placeholder': 'Describe why you are giving the badge',
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


class UserRangeRequestForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all().order_by('profile__user'), label="Seect the user")
    beginning = forms.DateTimeField(label="Start Date Time")
    end = forms.DateTimeField(label="End Date Time")



class MultiBadgeForm(forms.Form):
    awarded_by = forms.CharField(required=True)
    badge = forms.ModelChoiceField(queryset=Badge.objects.all(), required=True, label='Badge to be awarded')
    description = forms.CharField(widget=forms.Textarea(), label='Message to users')
    profiles = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=User.objects.all().order_by(Lower('profile__name')), required=True, label='Select the Profiles')
