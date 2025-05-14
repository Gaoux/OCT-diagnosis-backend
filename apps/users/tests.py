from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import UserAccount

User = get_user_model()

class UserAccountModelTest(APITestCase):
    def test_create_user(self):
        user = UserAccount.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            name='Test User',
            role='patient'
        )
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(user.role, 'patient')
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        admin = UserAccount.objects.create_superuser(
            email='admin@example.com',
            password='adminpass',
            name='Admin',
            role='admin'
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
        self.assertEqual(admin.role, 'admin')

class UserRegistrationAPITest(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'name': 'New User',
            'role': 'patient'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserAccount.objects.filter(email='newuser@example.com').exists())

    def test_register_duplicate_email(self):
        UserAccount.objects.create_user(email='dup@example.com', password='test', name='Dup', role='patient')
        url = reverse('register')
        data = {
            'email': 'dup@example.com',
            'password': 'test',
            'name': 'Dup',
            'role': 'patient'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

class UserLoginAPITest(APITestCase):
    def setUp(self):
        self.user = UserAccount.objects.create_user(
            email='loginuser@example.com',
            password='loginpass',
            name='Login User',
            role='patient',
            is_verified=True
        )

    def test_login_success(self):
        url = reverse('login')
        data = {'email': 'loginuser@example.com', 'password': 'loginpass'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_unverified(self):
        user = UserAccount.objects.create_user(
            email='unverified@example.com',
            password='test',
            name='Unverified',
            role='patient',
            is_verified=False
        )
        url = reverse('login')
        data = {'email': 'unverified@example.com', 'password': 'test'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('error', response.data)

    def test_login_wrong_password(self):
        url = reverse('login')
        data = {'email': 'loginuser@example.com', 'password': 'wrongpass'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

class UserProfileAPITest(APITestCase):
    def setUp(self):
        self.user = UserAccount.objects.create_user(
            email='profile@example.com',
            password='profilepass',
            name='Profile User',
            role='patient',
            is_verified=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        url = reverse('user-profile')
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_patch_profile(self):
        url = reverse('user-profile')
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'Updated Name')

class AdminRegistrationAPITest(APITestCase):
    def setUp(self):
        self.admin = UserAccount.objects.create_superuser(
            email='admin@test.com',
            password='adminpass',
            name='Admin',
            role='admin',
            is_admin=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)

    def test_admin_register(self):
        url = reverse('admin-register')
        data = {
            'email': 'newadmin@example.com',
            'password': 'adminpass',
            'name': 'New Admin'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserAccount.objects.filter(email='newadmin@example.com').exists())

class DashboardStatsAPITest(APITestCase):
    def setUp(self):
        self.admin = UserAccount.objects.create_superuser(
            email='admin2@test.com',
            password='adminpass',
            name='Admin2',
            role='admin',
            is_admin=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
        UserAccount.objects.create_user(email='p1@test.com', password='test', name='P1', role='patient')
        UserAccount.objects.create_user(email='p2@test.com', password='test', name='P2', role='patient')
        UserAccount.objects.create_user(email='pro@test.com', password='test', name='Pro', role='professional')

    def test_dashboard_stats(self):
        url = reverse('dashboard-stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_users', response.data)
        self.assertIn('total_patients', response.data)
        self.assertIn('total_ophthalmologists', response.data)
        self.assertIn('total_admins', response.data)
