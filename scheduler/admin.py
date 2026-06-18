from django.contrib import admin
from .models import ScheduledPost


@admin.register(ScheduledPost)
class ScheduledPostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "platform",
        "content",
        "status",
        "scheduled_time",
    )

    list_filter = (
        "platform",
        "status",
        "scheduled_time",
    )

    search_fields = (
        "user__username",
        "content__title",
    )

    ordering = ("-scheduled_time",)
