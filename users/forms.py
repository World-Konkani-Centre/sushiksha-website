from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models.functions import Lower
from .models import Profile, Reward, Mentions, Badge


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


class UserRangeRequestForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all().order_by('profile__user'), label="Seect the user")
    beginning = forms.DateTimeField(label="Start Date Time")
    end = forms.DateTimeField(label="End Date Time")


class MultiBadgeForm(forms.Form):
    choices = []
    for i in User.objects.all().order_by(Lower('profile__name')):
        name = str(i.profile.name) + '  (' + str(i.profile.get_team_name()) + ')'
        entry = (i.id, name)
        choices.append(entry)
    choices = tuple(choices)

    badge_choices = []
    for i in Badge.objects.all():
        name = str(i.title) + '  (' + str(i.points) + ')'
        entry = (i.id, name)
        badge_choices.append(entry)
    badge_choices = tuple(badge_choices)

    awarded_by = forms.CharField(required=True)
    badge = forms.ChoiceField(choices=badge_choices, required=True)
    description = forms.CharField(widget=forms.Textarea())
    profiles = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=choices, required=True)
