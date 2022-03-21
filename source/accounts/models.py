from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        related_name="profile",
        verbose_name="Profile",
        on_delete=models.CASCADE,
    )

    birth_date = models.DateField(
        null=True,
        blank=False,
        verbose_name="Birth date",
    )

    avatar = models.ImageField(
        verbose_name="Avatar",
        upload_to="avatars/",
        null=True,
        blank=False
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self) -> str:
        return f"Profile: {self.user.username}. {self.id}"