from django.db import models

from users.models import User


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Ticket(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 99,999,999.99
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")

    def __str__(self):
        return self.name


class Like(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["event", "user"], name="unique_like"),
        ]

    def __str__(self):
        return f'Event "{self.event}", User "{self.user}"'


class Comment(models.Model):
    text = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.text
