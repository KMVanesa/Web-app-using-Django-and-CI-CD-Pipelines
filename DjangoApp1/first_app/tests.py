from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse


# from model import Post
# from .forms import PostForm


class UnitTests(TestCase):
    def test_open_registration_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_open_login_page(self):
        response = self.client.get(reverse('home:login'))
        self.assertEqual(response.status_code, 200)

    def test_open_home_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
