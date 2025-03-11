from django.urls import path
from .views import PredictOCTView

urlpatterns = [
    path("predict/", PredictOCTView.as_view(), name="predict_oct"),  
]