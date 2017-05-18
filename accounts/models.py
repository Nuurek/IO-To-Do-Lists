from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings


class UserProfile(models.Model):
    """
    Couples user with their's account confirmation code.
    """
    user = models.OneToOneField(
        User,
        help_text="user owning the profile"
    )
    confirmation_code = models.CharField(
        blank=True,
        max_length=32,
        verbose_name="Confirmation code",
        help_text="used in account confirmation process"
    )

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        """Returns URL associated with UserProfile"""
        return reverse("user", kwargs={"user_id": self.user.pk})

    def send_confirmation_code(self):
        """
        Builds and sends email with confirmation code to user.
        Uses associated User `email_user` method.
        """
        self.user.email_user("Superlists - Email Verification",
                             "Please confirm your registration by clicking this link: "
                             + "http://"
                             + settings.ALLOWED_HOSTS[0]
                             + reverse("register_confirm", kwargs={
                                 "user_profile_id": self.id,
                                 "code": self.confirmation_code}))

    def activate_user(self):
        """
        Activates `User` associated with `UserProfile`.
        Should be used only after confirming the account with confirmation code.
        """
        self.user.is_active = True
        self.user.save()
