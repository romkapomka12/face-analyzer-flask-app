from flask import Flask, render_template, request, url_for
import base64
from tensorflow import keras
import numpy as np
from PIL import Image
import io
import logging


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

models = {}
CLASS_NAMES_GENDER = ['Female', 'Male'] # 0 = Female, 1 = Male

def load_all_models():
    """Завантажує AI моделі в пам'ять."""
    logging.info("Завантаження моделей...")
    try:
        
        models['gender'] = keras.models.load_model('models/gender_classifier_final.h5')
        logging.info(">>> Модель для гендеру завантажено!")
    except Exception as e:
        logging.error(f"!!! Помилка завантаження моделей: {e}")


@app.before_first_request
def before_first_request():
    load_all_models()


"""ГОЛОВНІ (ROUTES)"""
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
  if 'file' not in request.files or request.files['file'].filename == '':
        return "Помилка: файл не вибрано", 400

  file = request.files['file']
  results = {
        "race": {"prediction": "White", "confidence": "88.14%"},
        "gender": {"prediction": "Female", "confidence": "95.20%"},
        "age": {"prediction": 28}
    }





if __name__ == '__main__':
  app.run(debug=True)