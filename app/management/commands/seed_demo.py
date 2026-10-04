from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from app.models import Project, SiteProfile


PROFILE_NAME = "Alex Morgan (Demo)"

PROJECTS = (
    {
        "title": "Stockroom",
        "slug": "stockroom",
        "summary": "A clear, responsive inventory dashboard for small retail teams.",
        "description": (
            "Demo case study: Stockroom brings product search, stock levels, "
            "and low-stock reminders into one tidy workspace. The interface "
            "is designed to make common inventory tasks easy to find on both "
            "desktop and mobile."
        ),
        "technologies": "Django, Python, PostgreSQL, HTML, CSS",
        "image_path": "images/pic02.jpg",
        "is_featured": True,
        "display_order": 1,
    },
    {
        "title": "Atlas Notes",
        "slug": "atlas-notes",
        "summary": "A lightweight knowledge base for keeping ideas organized.",
        "description": (
            "Demo case study: Atlas Notes groups a team's notes by topic and "
            "makes them easy to search. Its focused layout keeps writing and "
            "reading comfortable, while simple organization helps useful "
            "information stay easy to find."
        ),
        "technologies": "Django, Python, SQLite, JavaScript",
        "image_path": "images/pic03.jpg",
        "is_featured": True,
        "display_order": 2,
    },
    {
        "title": "Studio Sessions",
        "slug": "studio-sessions",
        "summary": "A straightforward appointment-booking experience for a creative studio.",
        "description": (
            "Demo case study: Studio Sessions helps visitors explore services "
            "and request an appointment without a long back-and-forth. The "
            "booking flow keeps the next step clear and presents the studio's "
            "offerings in a polished, mobile-friendly format."
        ),
        "technologies": "Django, Python, HTML, CSS, PostgreSQL",
        "image_path": "images/pic04.jpg",
        "is_featured": True,
        "display_order": 3,
    },
    {
        "title": "Field Journal",
        "slug": "field-journal",
        "summary": "A photo-led journal for collecting notes from the outdoors.",
        "description": (
            "Demo case study: Field Journal pairs trip notes with photographs "
            "and location details in a calm, readable archive. Entries are "
            "designed to be easy to browse and enjoyable on smaller screens."
        ),
        "technologies": "Django, Python, SQLite, responsive web design",
        "image_path": "images/pic05.jpg",
        "is_featured": False,
        "display_order": 4,
    },
)


class Command(BaseCommand):
    help = "Add an illustrative portfolio profile and sample projects."

    @transaction.atomic
    def handle(self, *args, **options):
        existing_demo_profile = SiteProfile.objects.filter(
            display_name=PROFILE_NAME
        ).exists()
        if not existing_demo_profile and (
            SiteProfile.objects.exists() or Project.objects.exists()
        ):
            raise CommandError(
                "Existing profile or project content was found. "
                "The demo content was not added or changed."
            )

        profile, profile_created = SiteProfile.objects.get_or_create(
            display_name=PROFILE_NAME,
            defaults={
                "headline": (
                    "Full-stack developer building thoughtful, "
                    "reliable web experiences."
                ),
                "bio": (
                    "Welcome to this sample developer portfolio. Explore a "
                    "few illustrative projects, then use the contact form "
                    "to try the message flow. Replace this demo profile and "
                    "the sample case studies with your own details."
                ),
                "is_active": True,
            },
        )

        created_projects = 0
        for project_data in PROJECTS:
            _, created = Project.objects.get_or_create(
                slug=project_data["slug"],
                defaults={
                    **project_data,
                    "is_published": True,
                },
            )
            created_projects += created

        if profile_created or created_projects:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Demo content ready: "
                    f"{'created' if profile_created else 'kept'} profile "
                    f"and {created_projects} new project(s)."
                )
            )
        else:
            self.stdout.write("Demo content is already present; nothing changed.")
