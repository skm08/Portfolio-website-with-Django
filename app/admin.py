from django.contrib import admin

from .models import ContactMessage, Project, SiteProfile


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    list_display = ("display_name", "headline", "is_active")
    list_editable = ("is_active",)
    search_fields = ("display_name", "headline")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "is_featured", "display_order")
    list_filter = ("is_published", "is_featured")
    list_editable = ("is_published", "is_featured", "display_order")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "summary", "technologies")
    fieldsets = (
        (None, {"fields": ("title", "slug", "summary", "description")}),
        ("Media and links", {"fields": ("technologies", "image_path", "image_url", "live_url", "source_url")}),
        ("Publishing", {"fields": ("is_published", "is_featured", "display_order")}),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "name", "email", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    list_editable = ("is_read",)
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")
