from flask import Flask
from .models import Predict

app = Flask(__name__)
model = Predict()

from app import routes
