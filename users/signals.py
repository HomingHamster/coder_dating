from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from users.models import Profile, InterestedIn


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile(user=user, friendship=True).save()
        InterestedIn(user=profile.user, interest="tf").save()
        InterestedIn(user=profile.user, interest="tm").save()
        InterestedIn(user=profile.user, interest="m").save()
        InterestedIn(user=profile.user, interest="w").save()
        InterestedIn(user=profile.user, interest="nb").save()
    else:
        try:
            email = EmailAddress.objects.get_primary(user)
            if email.email != user.email:
                email.email = user.email
                email.verified = False
                email.save()
        except:
            EmailAddress(user=user, email=user.email, primary=True, verified=False).save()

@receiver(pre_save, sender=User)
def user_presave(sender, instance, **kwargs):
    if instance.username:
        instance.username = instance.username.lower()