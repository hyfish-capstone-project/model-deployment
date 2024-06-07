import tensorflow as tf
from tensorflow.keras.preprocessing import image
from google.cloud import storage
import numpy as np
from dotenv import load_dotenv
import string
import random
import os
import asyncio

class Predict:
    def __init__(self):
        self.class_labels = ['Black Sea Sprat', 'Gilt-Head Bream', 'Hourse Mackerel', 'Red Mullet', 'Red Sea Bream', 'Sea Bass', 'Shrimp', 'Striped Red Mullet', 'Trout']
        
        load_dotenv();
        self.bucket_name = os.environ.get("BUCKET_NAME")
        temp_name = self.create_suffix() + ".h5"
        asyncio.run(self.download_from_bucket(os.environ.get("CLASSIFIER_MODEL_PATH"), temp_name))
        self.model = tf.keras.models.load_model(temp_name)
        os.remove(temp_name)

    async def create_suffix(self):
        return ''.join(random.choice(string.ascii_letters) for i in range(14))

    async def download_from_bucket(self, srcpath, despath):
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(srcpath)
        blob.download_to_filename(despath)

    async def load_and_preprocess_image(self, image_file, target_size=(150, 150)):
        img = image.load_img(image_file, target_size=target_size)
        os.remove(image_file)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        return img_array

    async def predict_image(self, image_file):
        img_array = await self.load_and_preprocess_image(image_file)
        predictions = self.model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]
        predicted_label = self.class_labels[predicted_class]
        return predicted_label, predictions
    
    async def get_result(self, filepath):
        filename = self.create_suffix() + ".jpg"
        await self.download_from_bucket(filepath, filename)
        predicted_label, predictions = await self.predict_image(filename)
        return predicted_label, predictions
