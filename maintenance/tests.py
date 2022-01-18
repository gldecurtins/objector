from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
import rules
from .models import Work
from inventory.models import Object


class WorkRuleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.owner1 = User.objects.create_user(
            username="owner1@objector.com", email="owner1@objector.com", password="foo"
        )
        cls.owner2 = User.objects.create_user(
            username="owner2@objector.com", email="owner2@objector.com", password="foo"
        )
        cls.object = Object.objects.create(name="Object", owner=cls.owner1)
        cls.work = Work.objects.create(
            name="Work", object=cls.object, due_at=timezone.now()
        )

    def test_work_objekt_owner_permissions(self):
        self.assertEqual(
            rules.has_perm("journal.view_work", self.owner1, self.work),
            True,
        )
        self.assertEqual(
            rules.has_perm("journal.change_work", self.owner1, self.work),
            True,
        )
        self.assertEqual(
            rules.has_perm("journal.delete_work", self.owner1, self.work),
            True,
        )

    def test_work_objekt_non_owner_permissions(self):
        self.assertEqual(
            rules.has_perm("journal.view_work", self.owner2, self.work),
            False,
        )
        self.assertEqual(
            rules.has_perm("journal.change_work", self.owner2, self.work),
            False,
        )
        self.assertEqual(
            rules.has_perm("journal.delete_work", self.owner2, self.work),
            False,
        )
