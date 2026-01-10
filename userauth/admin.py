from django.contrib import admin

from .models import EmailVerification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = (
		"id",
		"email",
		"username",
		"role",
		"is_active",
		"is_email_verified",
		"date_joined",
	)
	search_fields = ("email", "username", "role")
	list_filter = ("role", "is_active", "is_email_verified")


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "token", "created_at")
	search_fields = ("user__email", "token")
