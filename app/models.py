import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.sequence import pad_sequences
from google.cloud import storage
import numpy as np
from dotenv import load_dotenv
import string
import random
import os
import asyncio
import joblib

class Predict:
    def __init__(self):
        self.class_labels = ['Black Sea Sprat', 'Gilt-Head Bream', 'Hourse Mackerel', 'Red Mullet', 'Red Sea Bream', 'Sea Bass', 'Shrimp', 'Striped Red Mullet', 'Trout']
        
        load_dotenv()
        self.bucket_name = os.environ.get("BUCKET_NAME")
        
        temp_name = self.create_suffix() + ".h5"
        self.download_from_bucket(os.environ.get("CLASSIFIER_MODEL_PATH"), temp_name)
        self.classifier_model = tf.keras.models.load_model(temp_name)
        os.remove(temp_name)

        temp_name = self.create_suffix() + ".h5"
        self.download_from_bucket(os.environ.get("FRESHNESS_MODEL_PATH"), temp_name)
        self.freshness_model = tf.keras.models.load_model(temp_name)
        os.remove(temp_name)

        temp_name = self.create_suffix() + ".h5"
        self.download_from_bucket(os.environ.get("TOXIC_MODEL_PATH"), temp_name)
        self.toxic_model = tf.keras.models.load_model(temp_name, compile=False)
        self.toxic_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        os.remove(temp_name)

        temp_name = self.create_suffix() + ".joblib"
        self.download_from_bucket(os.environ.get("TOXIC_TOKENIZER_PATH"), temp_name)
        with open(temp_name, 'rb') as handle:
            self.tokenizer = joblib.load(handle)
        os.remove(temp_name)

    def create_suffix(self):
        return ''.join(random.choice(string.ascii_letters) for i in range(14))

    def download_from_bucket(self, srcpath, despath):
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(srcpath)
        blob.download_to_filename(despath)
        return blob
    
    async def freshness_preprocessing(self, img_path, target_size=(150, 150)):
        img = image.load_img(img_path, target_size=target_size)
        os.remove(img_path)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.inception_v3.preprocess_input(img_array)
        return img_array

    async def predict_freshness(self, img_path):
        filename = self.create_suffix() + ".jpg"
        self.download_from_bucket(img_path, filename)

        img_array = await self.freshness_preprocessing(filename)
        prediction = self.freshness_model.predict(img_array)
        if prediction[0] > 0.5:
            predicted_class = "Not Fresh"
        else:
            predicted_class = "Fresh"
        return predicted_class, float(prediction[0])
    
    async def infer(self, sentence):
        sequences = self.tokenizer.texts_to_sequences([sentence])
        padded = pad_sequences(sequences, maxlen=36, padding='post', truncating='post')

        prob_num = self.toxic_model.predict(padded)[0][0] 
        if prob_num > 0.8 :
            return 'Toxic', float(prob_num)
        else:
            return 'Not Toxic', float(prob_num)

    async def calssifier_preprocessing(self, image_file, target_size=(150, 150)):
        img = image.load_img(image_file, target_size=target_size)
        os.remove(image_file)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        return img_array

    async def predict_image(self, image_file):
        img_array = await self.calssifier_preprocessing(image_file)
        predictions = self.classifier_model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]
        predicted_label = self.class_labels[predicted_class]
        return predicted_label, float(predictions[0][predicted_class])
    
    async def predict_fish(self, filepath):
        filename = self.create_suffix() + ".jpg"
        self.download_from_bucket(filepath, filename)
        predicted_label, predictions = await self.predict_image(filename)
        return predicted_label, predictions
