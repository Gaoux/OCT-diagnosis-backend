import os
from django.test import TestCase
from django.conf import settings
import numpy as np
import cv2
from .services import preprocess_image, predict_oct, LABELS

class OCTServicesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Configuración inicial: Crear una imagen de prueba (puede ser un mock)
        cls.test_image_path = os.path.join(settings.BASE_DIR, "test_data/test_oct_image.jpg")
        if not os.path.exists(cls.test_image_path):
            os.makedirs(os.path.dirname(cls.test_image_path), exist_ok=True)
            cv2.imwrite(cls.test_image_path, np.zeros((299, 299, 3), dtype=np.uint8))  # Imagen dummy

    def test_preprocess_image(self):
        """Verifica que la imagen se preprocese correctamente."""
        img = preprocess_image(self.test_image_path)
        self.assertEqual(img.shape, (1, 299, 299, 3))  # Batch, height, width, channels

    def test_predict_oct(self):
        """Verifica que la predicción devuelva un formato válido."""
        result = predict_oct(self.test_image_path)
        self.assertIn("prediction", result)
        self.assertIn("probabilities", result)
        self.assertTrue(result["prediction"] in LABELS)
        self.assertEqual(len(result["probabilities"]), len(LABELS))