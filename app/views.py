from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactMessageForm
from .models import Project, SiteProfile


def home(request):
    profile = SiteProfile.objects.filter(is_active=True).first()
    projects = Project.objects.filter(is_published=True, is_featured=True)
    return render(
        request,
        "index.html",
        {"profile": profile, "projects": projects},
    )


def project_list(request):
    profile = SiteProfile.objects.filter(is_active=True).first()
    projects = Project.objects.filter(is_published=True)
    return render(
        request,
        "projects.html",
        {"profile": profile, "projects": projects},
    )


def project_detail(request, slug):
    profile = SiteProfile.objects.filter(is_active=True).first()
    project = get_object_or_404(Project, slug=slug, is_published=True)
    return render(
        request,
        "project_detail.html",
        {"profile": profile, "project": project},
    )


def contact(request):
    profile = SiteProfile.objects.filter(is_active=True).first()
    form = ContactMessageForm(
        request.POST if request.method == "POST" else None
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Thanks for reaching out. Your message was received.")
        return redirect("contact")
    return render(request, "contact.html", {"profile": profile, "form": form})
