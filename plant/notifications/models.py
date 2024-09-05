from django.db import models

from plant.users.models import User


# Create your models here.
class Notification(models.Model):
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipient",
    )
    text = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_by",
    )
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.recipient} | {self.created_by} | {self.is_sent}"
