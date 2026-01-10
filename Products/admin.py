from django.contrib import admin

from .models import Products


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
	list_display = (
		"id",
		"name",
		"user",
		"price",
		"created_at",
		"deleted",
	)
	list_filter = ("deleted", "created_at")
	search_fields = ("name", "user__email")
