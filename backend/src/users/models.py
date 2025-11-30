from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    REQUIRED_FIELDS = []


class PurchasedTicket(models.Model):
    event = models.ForeignKey(
        "events.Event",
        on_delete=models.CASCADE,
        related_name="purchased_tickets_by_users",
    )
    ticket = models.ForeignKey(
        "events.Ticket", on_delete=models.CASCADE, related_name="purchased_by_users"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="purchased_tickets"
    )
    purchase_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Ticket "{self.ticket}" for Event "{self.event}", User "{self.user}"'
