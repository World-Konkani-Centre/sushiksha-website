from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Reward

#
# def get_user_list(user):
#     CHOICE = []
#     for i in user.objects.all():
#         print(type(i))
#         user_set = (i.username, i)
#         CHOICE.append(user_set)
#     return CHOICE


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
        fields = ['name', 'batch', 'phone', 'college',
                  'profession', 'address', 'guidance',
                  'linkedin', 'instagram', 'twitter',
                  'github', 'okr', 'facebook',
                  'image']


class RewardForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Describe why your are giving the badge',
        'rows': 4
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
        'rows': 2
    }))

    class Meta:
        model = Reward
        fields = ['user', 'description', 'badges']

    def __init__(self, *args, **kwargs):
        super(BadgeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            print(visible.form)
            visible.field.widget.attrs['class'] = 'fstdropdown-select'
