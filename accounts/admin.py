
from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "subscription_plan",
        "is_active",
        "created_at",
    )

    list_filter = (
        "subscription_plan",
        "is_active",
        "created_at",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

