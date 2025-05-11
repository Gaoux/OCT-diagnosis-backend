from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated  # Import the permission class
from rest_framework.parsers import MultiPartParser, FormParser
import os
from .services import predict_oct, reload_model
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.conf import settings
from rest_framework import status
import os

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
    def post(self, request):
        uploaded_file = request.FILES.get('model')
        if not uploaded_file:
            return Response({"error": "No se proporcionó ningún archivo."}, status=status.HTTP_400_BAD_REQUEST)

        # Ruta absoluta hacia apps/oct_analysis/model/oct_model.h5
        save_path = os.path.join(settings.BASE_DIR, 'apps', 'oct_analysis', 'model')
        os.makedirs(save_path, exist_ok=True)  # Crea el directorio si no existe

        model_path = os.path.join(save_path, 'oct_model.h5')

        with open(model_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        return Response({"message": "Modelo cargado correctamente."}, status=status.HTTP_200_OK)