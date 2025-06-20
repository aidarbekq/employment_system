from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Пользовательская модель:
      - username, email, password, first_name, last_name, etc. (унаследовано)
      - добавляем поле 'role': выпускник, работодатель, админ
    """
    class Roles(models.TextChoices):
        ALUMNI = "ALUMNI", "Alumni"
        EMPLOYER = "EMPLOYER", "Employer"
        ADMIN = "ADMIN", "Administrator"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.ALUMNI,
        help_text="Role of the user: Alumni, Employer, or Administrator"
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
