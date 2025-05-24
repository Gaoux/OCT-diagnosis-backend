import io
import json
import uuid
from unittest.mock import patch, MagicMock
from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from PIL import Image as PILImage
from apps.users.models import UserAccount
from .models import Report, Image
from .serializers import ReportSerializer

def create_mock_image():
    """Crea una imagen JPEG válida en memoria"""
    image = PILImage.new('RGB', (100, 100), color='red')
    image_io = io.BytesIO()
    image.save(image_io, format='JPEG')
    return SimpleUploadedFile(
        "test.jpg",
        image_io.getvalue(),
        content_type="image/jpeg"
    )

@override_settings(MEDIA_ROOT='/tmp/test_media')
class ReportSerializerTest(TestCase):
    def setUp(self):
        self.user = UserAccount.objects.create_user(
            email='test@example.com',
            password='testpass123',
            role='professional'
        )
        self.valid_data = {
            'image_file': create_mock_image(),
            'predicted_diagnostic': 'DME',
            'diagnostic_probabilities': json.dumps({'DME': 0.8, 'CNV': 0.2}),
            'file_path': 'memory_path.jpg',
            'file_format': 'JPEG',
            'file_size_kb': 100
        }

    def test_valid_serializer(self):
        serializer = ReportSerializer(
            data=self.valid_data,
            context={'request': MagicMock(user=self.user)}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)

@override_settings(MEDIA_ROOT='/tmp/test_media')
class ReportAPITest(APITestCase):
    def setUp(self):
        self.pro_user = UserAccount.objects.create_user(
            email='professional@test.com',
            password='testpass123',
            role='professional'
        )
        
        self.mock_image = create_mock_image()
        
        self.image = Image.objects.create(
            file_path="memory_path.jpg",
            file_format='JPEG',
            file_size_kb=100
        )
        
        self.report = Report.objects.create(
            user=self.pro_user,
            image=self.image,
            predicted_diagnostic='CNV',
            diagnostic_probabilities={'CNV': 0.9, 'DME': 0.1}
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.pro_user)

    def test_create_report(self):
        url = reverse('create-report')
        data = {
            'image_file': create_mock_image(),
            'predicted_diagnostic': 'DME',
            'diagnostic_probabilities': json.dumps({'DME': 0.8, 'CNV': 0.2}),
            'file_path': 'memory_path.jpg',
            'file_format': 'JPEG',
            'file_size_kb': 100
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    @patch('apps.reports.views.Report.objects.get')
    @patch('builtins.open', new_callable=MagicMock)
    def test_secure_media_view(self, mock_open, mock_get):
        # Configurar mock del reporte
        mock_report = MagicMock()
        mock_file = MagicMock()
        mock_file.path = '/fake/path.jpg'
        mock_report.image.image_file = mock_file
        mock_report.user = self.pro_user
        mock_get.return_value = mock_report
        
        # Configurar mock del archivo
        mock_file_obj = MagicMock()
        mock_file_obj.__enter__.return_value = io.BytesIO(b"fake_image_data")
        mock_open.return_value = mock_file_obj
        
        # Llamar a la vista
        url = reverse('report-image', kwargs={'report_id': self.report.id})
        response = self.client.get(url)
        
        # Verificaciones
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_get.assert_called_once_with(id=self.report.id, user=self.pro_user)
        mock_open.assert_called_once_with('/fake/path.jpg', 'rb')

class MockStorageTests(APITestCase):
    def setUp(self):
        self.user = UserAccount.objects.create_user(
            email='mockuser@test.com',
            password='testpass123',
            role='professional'
        )
        self.client.force_authenticate(user=self.user)

    @override_settings(MEDIA_ROOT='/tmp/test_media')
    def test_file_upload_in_memory(self):
        url = reverse('create-report')
        data = {
            'image_file': create_mock_image(),
            'predicted_diagnostic': 'DRUSEN',
            'diagnostic_probabilities': json.dumps({'DRUSEN': 0.7, 'NORMAL': 0.3}),
            'file_path': 'memory_path.jpg',
            'file_format': 'JPEG',
            'file_size_kb': 100
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)