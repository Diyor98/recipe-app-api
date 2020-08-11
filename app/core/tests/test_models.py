from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def sample_user(email='test@gmail.com',password='test123'):
    return get_user_model().objects.create_user(email,password)

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with email is successfull"""
        email = 'test@londonappdev.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email = email,
            password=password,
        )

        self.assertEquals(user.email,email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalized(self):
        """Test email for a new user is normalized"""
        email = "test@LONDONAPP.COM"
        user = get_user_model().objects.create_user(email,'test123')

        self.assertEquals(user.email,email.lower())

    def test_new_user_invalid_email(self):

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'test23')

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@london.com',
            'test123'
        )

        self.assertTrue(user.is_superuser) # is_superuser is included in permissions mixin
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        tag = models.Tag.objects.create(
            user = sample_user(),
            name = 'Vegan'
        )

        self.assertEquals(str(tag),tag.name)

    def test_ingredient_str(self):
        ingredient = models.Ingredient.objects.create(
            user = sample_user(),
            name = "Cucumber",
        )

        self.assertEquals(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        recipe = models.Recipe.objects.create(
            user = sample_user(),
            title = 'Steak and mushroom sauce',
            time_minutes = 5,
            price = 5.00
        )

        self.assertEqual(str(recipe),recipe.title)