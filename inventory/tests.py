from django.test import TestCase
from django.contrib.auth import get_user_model
import rules
from .models import Location, Objekt


class ObjektRuleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.owner1 = User.objects.create_user(
            username="owner1@objektor.com", email="owner1@objektor.com", password="foo"
        )
        cls.owner2 = User.objects.create_user(
            username="owner2@objektor.com", email="owner2@objektor.com", password="foo"
        )
        cls.objekt = Objekt.objects.create(name="objekt", owner=cls.owner1)

    def test_objekt_owner_permissions(self):
        self.assertEqual(
            rules.has_perm("inventory.view_objekt", self.owner1, self.objekt),
            True,
        )
        self.assertEqual(
            rules.has_perm("inventory.change_objekt", self.owner1, self.objekt),
            True,
        )
        self.assertEqual(
            rules.has_perm("inventory.delete_objekt", self.owner1, self.objekt),
            True,
        )

    def test_objekt_non_owner_permissions(self):
        self.assertEqual(
            rules.has_perm("inventory.view_objekt", self.owner2, self.objekt),
            False,
        )
        self.assertEqual(
            rules.has_perm("inventory.change_objekt", self.owner2, self.objekt),
            False,
        )
        self.assertEqual(
            rules.has_perm("inventory.delete_objekt", self.owner2, self.objekt),
            False,
        )


class LocationRuleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.owner1 = User.objects.create_user(
            username="owner1@objektor.com", email="owner1@objektor.com", password="foo"
        )
        cls.owner2 = User.objects.create_user(
            username="owner2@objektor.com", email="owner2@objektor.com", password="foo"
        )
        cls.location = Location.objects.create(name="location", owner=cls.owner1)

    def test_location_owner_permissions(self):
        self.assertEqual(
            rules.has_perm("inventory.view_location", self.owner1, self.location),
            True,
        )
        self.assertEqual(
            rules.has_perm("inventory.change_location", self.owner1, self.location),
            True,
        )
        self.assertEqual(
            rules.has_perm("inventory.delete_location", self.owner1, self.location),
            True,
        )

    def test_location_non_owner_permissions(self):
        self.assertEqual(
            rules.has_perm("inventory.view_location", self.owner2, self.location),
            False,
        )
        self.assertEqual(
            rules.has_perm("inventory.change_location", self.owner2, self.location),
            False,
        )
        self.assertEqual(
            rules.has_perm("inventory.delete_location", self.owner2, self.location),
            False,
        )
