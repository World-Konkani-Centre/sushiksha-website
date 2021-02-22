from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Sum
from PIL import Image

ROLE = (
    ('Mentee', "Mentee"),
    ('Mentor', "Mentor"),
)

UPGRADE_POINTS = [
    [500, 1000, 2000, 5000, 2000, 3000, 5000],
    [1000, 3000, 5000, 15000, 4000, 5000, 10000],
]

# UPGRADE_POINTS = [
#     [0, 0, 0, 10815, 0, 21, 1004],
#     [0, 0, 0, 10815, 0, 21, 1004],
# ]

RANK = (
    ('Sophist', 'Sophist'),
    ('Senator', 'Senator'),
    ('Caesar', 'Caesar'),
)

BATCH = (
    ("2010", "2010"),
    ("2011", "2011"),
    ("2012", "2012"),
    ("2013", "2013"),
    ("2014", "2014"),
    ("2015", "2015"),
    ("2016", "2016"),
    ("2017", "2017"),
    ("2018", "2018"),
    ("2019", "2019"),
    ("2020", "2020"),
    ("2021", "2021"),
    ("None", "None"),
)


class Profile(models.Model):
    slack_id = models.CharField(max_length=15, null=True,blank=True,help_text="Slack Id of user")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    role = models.BooleanField(default=False)
    batch = models.CharField(max_length=10, choices=BATCH, default="2019")
    name = models.CharField(max_length=100, default=None, blank=True, null=True)
    phone = models.PositiveBigIntegerField(default=None, blank=True, null=True)
    college = models.CharField(max_length=300, default=None, blank=True, null=True)
    degree = models.CharField(max_length=100, default=None, blank=True, null=True)
    branch = models.CharField(max_length=100, default=None, blank=True, null=True)
    profession = models.CharField(max_length=100, default=None, blank=True, null=True)
    address = models.TextField(default=None, blank=True, null=True)
    guidance = models.TextField(default=None, blank=True, null=True)
    linkedin = models.URLField(default=None, blank=True, null=True)
    instagram = models.URLField(default=None, blank=True, null=True)
    twitter = models.URLField(default=None, blank=True, null=True)
    github = models.URLField(default=None, blank=True, null=True)
    okr = models.URLField(default=None, blank=True, null=True)
    facebook = models.URLField(default=None, blank=True, null=True)
    initiator = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    suShells = models.IntegerField(default=0)
    rank = models.CharField(max_length=10, choices=RANK, default='Sophist')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'pk': self.user.pk})

    def get_point(self):
        point = self.user.reward_set.aggregate(Sum('badges__points'))['badges__points__sum']
        if point:
            self.points = point
            self.save()
            return self.points
        else:
            self.points = 0
            self.save()
            return 0

    def get_team_name(self):
        team = self.teams_set.first()
        if team:
            return team.name
        else:
            return ''

    def get_team_url(self):
        team = self.teams_set.first()
        if team:
            return team.get_absolute_url()

    def get_house_name(self):
        team = self.teams_set.first()
        if team:
            team = team.house_set.first()
            if team:
                return team.name
            else:
                return ''
        else:
            return ''

    def get_house_url(self):
        team = self.teams_set.first()
        if team:
            team = team.house_set.first()
            if team:
                return team.get_absolute_url()

    @property
    def get_number_of_badges(self):
        return self.user.reward_set.count()

    @property
    def get_role(self):
        if self.role:
            return 'Mentor'
        else:
            return 'Mentee'


class Pomodoro(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField(default=0)
    energy = models.FloatField(default=0)
    productivity = models.FloatField(default=0)

    def __str__(self):
        return f'{self.user.username} - Pomodoro Count : {self.count}'


class BadgeCategory(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class Badge(models.Model):
    points = models.IntegerField(default=1)
    title = models.CharField(max_length=30)
    category = models.ForeignKey(BadgeCategory, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=500)
    logo = models.ImageField(upload_to='badges')
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f'{self.title} ({self.points})'


class Reward(models.Model):
    awarded_by = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    decision = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    badges = models.ForeignKey(Badge, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'


class Teams(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='teams')
    bio = models.TextField()
    points = models.IntegerField(default=0)
    members = models.ManyToManyField(Profile)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('team', kwargs={'id': self.pk})


class House(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='house')
    bio = models.TextField()
    points = models.IntegerField(default=0)
    teams = models.ManyToManyField(Teams)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('house', kwargs={'id': self.pk})


class Mentions(models.Model):
    image = models.ImageField(upload_to='mentions')
    title = models.CharField(max_length=100)
    team = models.ForeignKey(Teams, null=True, blank=True, on_delete=models.CASCADE)
    house = models.ForeignKey(House, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, default='description', null=True, blank=True)

    def __str__(self):
        return f'{self.title}'
