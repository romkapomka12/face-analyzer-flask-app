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



@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files or request.files['file'].filename == '':
        return "Помилка: файл не вибрано", 400

    file = request.files['file']
    image_bytes = file.read()
    processed_image = preprocess_image(image_bytes)
    

    logging.info("Починаємо аналіз гендеру...")
    pred_gender = models['gender'].predict(processed_image)[0][0]
    predicted_gender = CLASS_NAMES_GENDER[1] if pred_gender > 0.5 else CLASS_NAMES_GENDER[0]
    confidence_gender = f"{pred_gender:.2%}" if predicted_gender == 'Male' else f"{(1-pred_gender):.2%}"
    logging.info(f"Гендер: {predicted_gender} ({confidence_gender})")
    

    results = {
        "race": {"prediction": "White (mock)", "confidence": "N/A"},
        "gender": {"prediction": predicted_gender, "confidence": confidence_gender},
        "age": {"prediction": "28 (mock)"}
    }

    
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    return render_template('result.html', results=results, image_file=image_base64)




if __name__ == '__main__':
  app.run(debug=True)