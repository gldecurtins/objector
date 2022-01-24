from django.test import Client, TestCase
from .models import Team
from django.contrib.auth import get_user_model


class NoAccessTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_no_access_team_create(self):
        response = self.client.get("/team/add/")
        self.assertEqual(response.status_code, 302)

    def test_no_access_team_list(self):
        response = self.client.get("/team/")
        self.assertEqual(response.status_code, 302)


class TeamCreateTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user1, created = User.objects.get_or_create(
            username="user1@objector.local",
            email="user1@objector.local",
            password="foo",
        )
        self.client1 = Client()
        self.client1.force_login(self.user1)

    def test_team_create_access(self):
        response = self.client1.get("/team/add/")
        self.assertTemplateUsed(response, "common/team_form.html")
        self.assertContains(response, "name")
        self.assertContains(response, "description")
        self.assertContains(response, "image")
        self.assertContains(response, "owner")
        self.assertEqual(response.status_code, 200)

    def test_team_create_form(self):
        response = self.client1.post(
            "/team/add/",
            {"name": ""},
        )
        self.assertContains(response, "This field is required")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Team.objects.count(), 0)

    def test_team_create_form_ok(self):
        name = "test team name"
        description = "test team description"
        owner = self.user1
        self.client1.post(
            "/team/add/",
            {
                "name": name,
                "description": description,
                "owner": owner.id,
            },
        )
        self.assertEqual(
            Team.objects.filter(
                name=name, description=description, owner=self.user1
            ).count(),
            1,
        )
