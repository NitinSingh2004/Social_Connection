from django.contrib import admin
from .models import SocialAccount


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "platform",
        "account_name",
        "account_id",
        "access_token",
        "page_access_token",
        "created_at",
    )

    list_filter = (
        "platform",
        "created_at",
    )

    search_fields = (
        "user__username",
        "account_name",
        "account_id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)