from django.urls import path
from .views import PredictOCTView, UploadModelView

urlpatterns = [
    path("predict/", PredictOCTView.as_view(), name="predict_oct"), 
    path('upload-model/', UploadModelView.as_view(), name='upload-model'), 
]