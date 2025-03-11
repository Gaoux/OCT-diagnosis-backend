from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
import os
from .services import predict_oct

class PredictOCTView(APIView):
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
