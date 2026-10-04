from django.core.management import call_command, CommandError
from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage, Project, SiteProfile


class PortfolioViewsTests(TestCase):
    def setUp(self):
        self.profile = SiteProfile.objects.create(
            display_name="Ada Example",
            headline="Software developer",
            bio="I build useful software.",
            is_active=True,
        )
        self.featured_project = Project.objects.create(
            title="Featured project",
            slug="featured-project",
            summary="A featured project.",
            description="Project details.",
            is_featured=True,
            is_published=True,
        )
        self.unpublished_project = Project.objects.create(
            title="Draft project",
            slug="draft-project",
            summary="A draft project.",
            description="Not public yet.",
        )

    def test_homepage_shows_profile_and_published_featured_projects(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ada Example")
        self.assertContains(response, "Featured project")
        self.assertNotContains(response, "Draft project")

    def test_project_list_hides_unpublished_projects(self):
        response = self.client.get(reverse("project-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Featured project")
        self.assertNotContains(response, "Draft project")

    def test_only_published_projects_have_public_detail_pages(self):
        response = self.client.get(
            reverse("project-detail", args=[self.featured_project.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Project details.")

        response = self.client.get(
            reverse("project-detail", args=[self.unpublished_project.slug])
        )
        self.assertEqual(response.status_code, 404)

    def test_valid_contact_message_is_saved_and_redirects(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Visitor",
                "email": "visitor@example.com",
                "subject": "Project enquiry",
                "message": "Could we work together?",
            },
        )

        self.assertRedirects(response, reverse("contact"))
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(
            ContactMessage.objects.get().email,
            "visitor@example.com",
        )

    def test_invalid_contact_message_is_not_saved(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Visitor",
                "email": "not-an-email",
                "subject": "Question",
                "message": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertContains(response, "Enter a valid email address.")


class DemoSeedCommandTests(TestCase):
    def test_seed_command_creates_attractive_demo_content(self):
        call_command("seed_demo")

        profile = SiteProfile.objects.get()
        projects = Project.objects.filter(is_published=True)
        self.assertIn("(Demo)", profile.display_name)
        self.assertEqual(projects.count(), 4)
        self.assertEqual(projects.filter(is_featured=True).count(), 3)
        self.assertTrue(projects.filter(image_path__startswith="images/").exists())

        response = self.client.get(reverse("home"))
        self.assertContains(response, "Stockroom")
        self.assertContains(response, "/static/images/pic02.jpg")

    def test_seed_command_is_idempotent_and_keeps_admin_edits(self):
        call_command("seed_demo")
        profile = SiteProfile.objects.get()
        profile.headline = "My own headline"
        profile.save()
        project = Project.objects.get(slug="stockroom")
        project.summary = "My own project summary"
        project.save()

        call_command("seed_demo")

        self.assertEqual(SiteProfile.objects.count(), 1)
        self.assertEqual(Project.objects.count(), 4)
        self.assertEqual(SiteProfile.objects.get().headline, "My own headline")
        self.assertEqual(
            Project.objects.get(slug="stockroom").summary,
            "My own project summary",
        )

    def test_seed_command_refuses_to_mix_with_existing_personal_content(self):
        SiteProfile.objects.create(
            display_name="My profile",
            headline="My headline",
        )

        with self.assertRaisesMessage(CommandError, "Existing profile or project"):
            call_command("seed_demo")

        self.assertEqual(Project.objects.count(), 0)
