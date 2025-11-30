from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import PurchasedTicket, User


@admin.register(User)
class UserAdmin(UserAdmin):
    pass


@admin.register(PurchasedTicket)
class PurchasedTicketAdmin(admin.ModelAdmin):
    pass
