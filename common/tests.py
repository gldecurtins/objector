from django.test import Client, SimpleTestCase, TransactionTestCase
from django.urls import reverse
from .models import Team
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.utils.lorem_ipsum import words


class NoAccessTest(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_no_access_team_create(self):
        url = reverse("common:team-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_no_access_team_list(self):
        url = reverse("common:team-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class TeamCreateTest(TransactionTestCase):
    def setUp(self):
        User = get_user_model()
        self.user1, created = User.objects.get_or_create(
            username="user1@objector.local",
            email="user1@objector.local",
            password="foo",
        )
        self.client1 = Client()
        self.client1.force_login(self.user1)

        self.name_3 = words(3)
        self.name_4 = words(4)
        self.description_3 = words(3)

    def test_team_create_access(self):
        url = reverse("common:team-create")
        response = self.client1.get(url)
        self.assertTemplateUsed(response, "common/team_form.html")
        self.assertContains(response, "name")
        self.assertContains(response, "description")
        self.assertContains(response, "image")
        self.assertContains(response, "owner")
        self.assertEqual(response.status_code, 200)

    def test_team_get_create_form(self):
        url = reverse("common:team-create")
        response = self.client1.post(
            url,
            {"name": ""},
        )
        self.assertContains(response, "This field is required")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Team.objects.count(), 0)


class TeamUpdateTest(TransactionTestCase):
    def setUp(self):
        User = get_user_model()
        self.user1, created = User.objects.get_or_create(
            username="user1@objector.local",
            email="user1@objector.local",
            password="foo",
        )
        self.client1 = Client()
        self.client1.force_login(self.user1)

        self.name_3 = words(3)
        self.name_4 = words(4)
        self.description_3 = words(3)

    def test_team_update_form(self):
        url = reverse("common:team-create")
        self.client1.post(
            url,
            {
                "name": self.name_3,
                "description": self.description_3,
                "owner": self.user1.id,
            },
        )
        self.assertEqual(
            Team.objects.filter(
                name=self.name_3, description=self.description_3, owner=self.user1
            ).count(),
            1,
        )
        self.assertEqual(Group.objects.filter(name=self.name_3).count(), 1)
        self.assertEqual(Group.objects.filter(name=self.name_4).count(), 0)
        team_pk = Team.objects.get(name=self.name_3).pk
        url = reverse("common:team-update", kwargs={"pk": team_pk})
        response = self.client1.get(url)
        self.assertTemplateUsed(response, "common/team_form.html")
        self.assertContains(response, "name")
        self.assertContains(response, self.name_3)
        self.assertContains(response, "description")
        self.assertContains(response, self.description_3)
        self.assertContains(response, "image")
        self.assertContains(response, "owner")

        # New Team and Group in place
        response = self.client1.post(
            url,
            {
                "name": self.name_4,
                "description": self.description_3,
                "owner": self.user1.id,
            },
        )
        self.assertEqual(
            Team.objects.filter(
                name=self.name_4, description=self.description_3, owner=self.user1
            ).count(),
            1,
        )
        self.assertEqual(Group.objects.filter(name=self.name_4).count(), 1)

        # Previous Team- and Group-name no longer available
        self.assertEqual(Group.objects.filter(name=self.name_3).count(), 0)
        self.assertEqual(
            Team.objects.filter(
                name=self.name_4, description=self.description_3, owner=self.user1
            ).count(),
            1,
        )
