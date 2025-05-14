import os
import cv2
import numpy as np
from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.core.files.uploadedfile import SimpleUploadedFile

# Configuración inicial para Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from apps.oct_analysis.services import (
    preprocess_image,
    predict_oct,
    LABELS,
    model
)

class OCTServicesTest(TestCase):
    """Pruebas para el módulo de análisis OCT."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Crear imagen dummy para pruebas
        cls.test_image_path = "test_image.jpg"
        cv2.imwrite(cls.test_image_path, np.zeros((299, 299, 3), dtype=np.uint8))

    @classmethod
    def tearDownClass(cls):
        # Limpiar archivo dummy
        if os.path.exists(cls.test_image_path):
            os.remove(cls.test_image_path)
        super().tearDownClass()

    def test_preprocess_image_valid_input(self):
        """Verifica el preprocesamiento con imagen válida."""
        img = preprocess_image(self.test_image_path)
        self.assertEqual(img.shape, (1, 299, 299, 3))

    def test_preprocess_image_invalid_path(self):
        """Verifica manejo de rutas de imagen inválidas."""
        with self.assertRaises(Exception):
            preprocess_image("invalid_path.jpg")

    @patch('apps.oct_analysis.services.model.predict')
    def test_predict_oct_structure(self, mock_predict):
        """Valida la estructura del resultado de predicción."""
        # Configurar mock
        mock_predict.return_value = np.array([[0.1, 0.7, 0.1, 0.1]])  # Probabilidades simuladas
        
        result = predict_oct(self.test_image_path)
        
        # Validar estructura
        self.assertIn("prediction", result)
        self.assertIn("probabilities", result)
        self.assertEqual(len(result["probabilities"]), len(LABELS))

    @patch('apps.oct_analysis.services.model.predict')
    def test_predict_oct_label_mapping(self, mock_predict):
        """Verifica que las etiquetas se mapeen correctamente."""
        # Simular predicción para DME (segunda etiqueta)
        mock_predict.return_value = np.array([[0.0, 1.0, 0.0, 0.0]])
        
        result = predict_oct(self.test_image_path)
        self.assertEqual(result["prediction"], "DME")

    def test_model_loading(self):
        """Verifica que el modelo se cargue correctamente."""
        self.assertTrue(hasattr(model, 'predict'))
        self.assertEqual(model.optimizer.__class__.__name__, "Adam")

    @patch('cv2.imread')
    def test_corrupt_image_handling(self, mock_imread):
        """Prueba manejo de imágenes corruptas."""
        mock_imread.return_value = None  # Simular fallo de carga
        
        with self.assertRaises(Exception):
            preprocess_image(self.test_image_path)