from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientsApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email = 'test@gmail.com',
            password = 'test123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        Ingredient.objects.create(user=self.user,name="kale")
        Ingredient.objects.create(user=self.user, name='salt')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients,many=True)
        
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data,serializer.data)

    def test_ingredients_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            "test2@gmail.com",
            'testpass'
        )

        Ingredient.objects.create(user = user2, name='Something')

        ingredient = Ingredient.objects.create(user = self.user, name='Tumeric')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEquals(len(res.data),1)
        self.assertEquals(res.data[0]['name'],ingredient.name)


    def test_create_ingredient_successful(self):
        payload = {'name' : 'Cabbage'}
        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(user = self.user,
                                            name = payload['name'],).exists()

        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        payload = {'name' : ''}
        rec = self.client.post(INGREDIENTS_URL,payload)

        self.assertEquals(rec.status_code, status.HTTP_400_BAD_REQUEST)