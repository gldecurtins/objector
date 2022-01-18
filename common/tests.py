from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.


class UserTest(TestCase):
    def test_create_owner1(self):
        User = get_user_model()
        self.owner1 = User.objects.create_user(
            username="owner1@objektor.com", email="owner1@objektor.com", password="foo"
        )
        self.assertEqual(self.owner1.email, "owner1@objektor.com")
        self.assertFalse(self.owner1.is_staff)
        self.assertFalse(self.owner1.is_superuser)

    def test_create_owner2(self):
        User = get_user_model()
        self.owner2 = User.objects.create_user(
            username="owner2@objektor.com", email="owner2@objektor.com", password="foo"
        )
        self.assertEqual(self.owner2.email, "owner2@objektor.com")
        self.assertFalse(self.owner2.is_staff)
        self.assertFalse(self.owner2.is_superuser)
