from django.conf import settings
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]


class ScheduledPost(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    content = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )

    platform = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    scheduled_time = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        default="scheduled"
    )

    def __str__(self):
        return f"{self.user} - {self.status}"
