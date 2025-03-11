import tensorflow as tf
import numpy as np
import os
from keras.optimizers import Adam
from django.conf import settings
import cv2

# Load the model once when the app starts
MODEL_PATH = os.path.join(settings.BASE_DIR, "apps/oct_analysis/model/oct_model.h5")

model = tf.keras.models.load_model(MODEL_PATH, compile=False)  # Load the pre-trained model

# Recompile the model
model.compile(optimizer=Adam(learning_rate=0.001),  
              loss='categorical_crossentropy',  
              metrics=['accuracy']) 
# Define labels
LABELS = ["CNV", "DME", "DRUSEN", "NORMAL"]

def preprocess_image(image_path, target_size=(299, 299)):
    """Loads and preprocesses an image for prediction."""
    img = cv2.imread(image_path)  # Load image
    img = cv2.resize(img, target_size)  # Resize to model input size
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

def predict_oct(image_path):
    """Returns the predicted class and probabilities for an OCT image."""
    img = preprocess_image(image_path)
    predictions = model.predict(img)[0]  # Get probability distribution
    predicted_label = LABELS[np.argmax(predictions)]  # Get highest probability label
    return {"prediction": predicted_label, "probabilities": predictions.tolist()}
