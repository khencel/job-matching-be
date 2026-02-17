from django.contrib import admin

from .models import JobPost


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
	list_display = (
		"id",
		"title",
		"user_id",
		"salary",
		"created_at",
		"deleted",
	)
	list_filter = ("deleted", "created_at")
	search_fields = ("title", "user_id")
