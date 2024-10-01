from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Item
from django.contrib.auth.models import User

# class ItemTests(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.client.login(username='testuser', password='testpassword')

#     def test_create_item(self):
#         response = self.client.post('/api/items/', {'name': 'Item1', 'description': 'Item1 description'})
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_get_item(self):
#         item = Item.objects.create(name='Item2', description='Item2 description')
#         response = self.client.get(f'/api/items/{item.id}/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_update_item(self):
#         item = Item.objects.create(name='Item3', description='Item3 description')
#         response = self.client.put(f'/api/items/{item.id}/', {'name': 'Updated Item3', 'description': 'Updated description'})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_delete_item(self):
#         item = Item.objects.create(name='Item4', description='Item4 description')
#         response = self.client.delete(f'/api/items/{item.id}/')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
