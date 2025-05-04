from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated  # Import the permission class
from rest_framework.parsers import MultiPartParser, FormParser
import os
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.conf import settings

from .services import predict_oct

class PredictOCTView(APIView):
    permission_classes = [IsAuthenticated]  # This line ensures the user must be authenticated with JWT
    
    parser_classes = (MultiPartParser, FormParser)  # Handles file uploads

    def post(self, request):
        """API endpoint for OCT image classification."""
        if "image" not in request.FILES:
            return JsonResponse({"error": "No image uploaded"}, status=400)

        image = request.FILES["image"]

        # Save the image temporarily
        image_path = f"temp_{image.name}"
        with open(image_path, "wb") as f:
            for chunk in image.chunks():
                f.write(chunk)

        # Run prediction
        result = predict_oct(image_path)

        # Clean up (optional)
        os.remove(image_path)

        return JsonResponse(result)

class UploadModelView(APIView):
    """
    Endpoint para que los administradores carguen un nuevo archivo .h5
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No se proporcionó ningún archivo."}, status=400)

        if not file.name.endswith('.h5'):
            return Response({"error": "El archivo debe tener la extensión .h5."}, status=400)

        # Ruta donde se guardará el archivo
        model_path = os.path.join(settings.BASE_DIR, "apps/oct_analysis/model/oct_model.h5")

        # Reemplaza el archivo existente
        with open(model_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        return Response({"message": "El archivo .h5 se cargó y reemplazó correctamente."}, status=200)
