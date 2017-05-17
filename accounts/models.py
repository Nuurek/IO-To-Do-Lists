from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings


class UserProfile(models.Model):
    """
    Couples user with their's account confirmation code.

    Attributes:
        user - user owning the profile
        confirmation_code - code used in account confirmation process
    """
    user = models.OneToOneField(User)
    confirmation_code = models.CharField(blank=True, max_length=32)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("user", kwargs={"user_id": self.user.pk})

    def send_confirmation_code(self):
        self.user.email_user("Superlists - Email Verification",
                             "Please confirm your registration by clicking this link: "
                             + "http://"
                             + settings.ALLOWED_HOSTS[0]
                             + reverse("register_confirm", kwargs={
                                 "user_profile_id": self.id,
                                 "code": self.confirmation_code}))

    def activate_user(self):
        self.user.is_active = True
        self.user.save()
