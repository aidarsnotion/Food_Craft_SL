import unittest
from django.test import RequestFactory

from .tes import authorization

class AuthorizationTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_successful_login(self):
        request = self.factory.post('/login/', {'username': 'testuser', 'password': 'testpass'})
        result = authorization(request)
        self.assertEqual(result, "Success!")
    
    def test_invalid_credentials(self):
        request = self.factory.post('/login/', {'username': 'testuser', 'password': 'wrongpass'})
        result = authorization(request)
        self.assertEqual(result, "Неверный логин или пароль!")
    
    def test_missing_username(self):
        request = self.factory.post('/login/', {'password': 'testpass'})
        result = authorization(request)
        self.assertEqual(result, "Введите Username или E-mail")
    
    def test_missing_password(self):
        request = self.factory.post('/login/', {'username': 'testuser'})
        result = authorization(request)
        self.assertEqual(result, "Введите пароль")
    
    def test_invalid_username_password(self):
        request = self.factory.post('/login/', {'username': 'nonexistent', 'password': 'wrongpass'})
        result = authorization(request)
        self.assertEqual(result, "Неверный логин или пароль!")

    