from django.conf import settings
from django.db import models

from users.models import User


class Event(models.Model):
    # Category choices for reference/validation
    CATEGORY_CHOICES = [
        ("festival", "Festival"),
        ("concert", "Concert"),
        ("conference", "Conference"),
        ("workshop", "Workshop"),
        ("sports", "Sports"),
        ("theater", "Theater"),
        ("exhibition", "Exhibition"),
        ("charity", "Charity"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default="other"
    )

    def __str__(self):
        return self.name


class Ticket(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
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


class SavedEvent(models.Model):
    """Track events saved by users"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_events"
    )
    event = models.ForeignKey(
        "Event",
        on_delete=models.CASCADE,
        related_name="saved_by_users",
    )
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")
        ordering = ["-saved_at"]

    def __str__(self):
        return f"{self.user.username} saved {self.event.name}"
