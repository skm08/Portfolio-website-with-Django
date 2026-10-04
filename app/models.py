from django.db import models


class SiteProfile(models.Model):
    display_name = models.CharField(max_length=100)
    headline = models.CharField(max_length=180)
    bio = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    resume_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-is_active", "pk")
        verbose_name = "site profile"
        verbose_name_plural = "site profile"

    def __str__(self):
        return self.display_name


class Project(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    summary = models.CharField(max_length=280)
    description = models.TextField()
    technologies = models.CharField(
        max_length=300,
        blank=True,
        help_text="Separate technologies with commas.",
    )
    image_path = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional image path relative to static/, such as images/pic03.jpg.",
    )
    image_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    source_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("display_order", "-created_at")

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=160)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.subject} — {self.name}"
