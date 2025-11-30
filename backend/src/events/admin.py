from django.contrib import admin

from events.models import Comment, Event, Like, Ticket


class TicketInline(admin.StackedInline):
    model = Ticket
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [TicketInline]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
