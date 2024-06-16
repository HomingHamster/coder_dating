from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.templatetags.static import static


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=80, blank=True, null=True, verbose_name="Display Name")
    image = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Display Pic')
    bio = models.TextField(blank=True, null=True)
    friendship = models.BooleanField(default=True)
    love = models.BooleanField(default=False, verbose_name="Love (18+)")
    working = models.BooleanField(default=False)
    hiring = models.BooleanField(default=False)
    gender = models.CharField(max_length=2, blank=True, null=True,
                              choices=[('tw', 'Transfem'),
                                       ('tm', 'Transmasc'),
                                       ('m', 'Man'),
                                       ('w', 'Woman'),
                                       ('nb', 'Non-Binary')])
    age = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(120), MinValueValidator(0)])

    def __str__(self):
        return self.name

    @property
    def name(self):
        if self.display_name:
            return self.display_name
        else:
            return self.user.username

    @property
    def avatar(self):
        try:
            return self.image.url
        except ValueError:
            return static("images/avatar.svg")


class InterestedIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.CharField(max_length=2, choices=[('tw', 'Transfem'),
                                                       ('tm', 'Transmasc'),
                                                       ('m', 'Men'),
                                                       ('w', 'Women'),
                                                       ('nb', 'Non-Binary')])

    class Meta:
        unique_together = (('user', 'interest'),)

    def __str__(self):
        return f"{self.user.profile.name} is interested in {self.interest}"