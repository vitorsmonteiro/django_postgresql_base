from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from authentication.forms import CreateUserForm, CustomUserChangeForm
from authentication.models import User


class UserAdmin(BaseUserAdmin):
    """Custom UserAdmin for the custom User model."""

    form = CustomUserChangeForm
    add_form = CreateUserForm

    list_display = ("email", "first_name", "last_name", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser", "groups")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "profile_image")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions")


admin.site.register(User, UserAdmin)
