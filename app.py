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
CLASS_NAMES_RACE = ['White', 'Black', 'East Asian', 'Indian', 'Southeast Asian', 'Middle Eastern', 'Latino_Hispanic']
CLASS_NAMES_GENDER = ['Female', 'Male']


def load_all_models():
    logging.info("Завантаження всіх моделей...")
    try:
        models['race'] = keras.models.load_model('models/race_classifier_best.h5')
        models['gender'] = keras.models.load_model('models/gender_classifier_final.h5')
        models['age'] = keras.models.load_model('models/age_predictor_final.h5')
        logging.info("Усі моделі успішно завантажено!")
    except Exception as e:
        logging.error(f"!!! Помилка завантаження моделей: {e}")


@app.before_first_request
def before_first_request():
    load_all_models()


def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


# --- 4. ГОЛОВНІ ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files or request.files['file'].filename == '':
        return "Помилка: файл не вибрано", 400

    file = request.files['file']
    image_bytes = file.read()
    processed_image = preprocess_image(image_bytes)
    
    # --- РЕАЛЬНА РОБОТА ВСІХ МОДЕЛЕЙ ---
    logging.info("Пповний аналіз зображення...")

    # Раса
    pred_race = models['race'].predict(processed_image)[0]
    predicted_race = CLASS_NAMES_RACE[np.argmax(pred_race)]
    confidence_race = f"{np.max(pred_race):.2%}"
    logging.info(f"Раса: {predicted_race} ({confidence_race})")

    # Гендер
    pred_gender = models['gender'].predict(processed_image)[0][0]
    predicted_gender = CLASS_NAMES_GENDER[1] if pred_gender > 0.5 else CLASS_NAMES_GENDER[0]
    confidence_gender = f"{pred_gender:.2%}" if predicted_gender == 'Male' else f"{(1-pred_gender):.2%}"
    logging.info(f"Гендер: {predicted_gender} ({confidence_gender})")

    # Вік
    pred_age = models['age'].predict(processed_image)[0][0]
    predicted_age = round(pred_age)
    logging.info(f"Вік: ~{predicted_age} років")
    
    # Результати
    results = {
        "race": {"prediction": predicted_race, "confidence": confidence_race},
        "gender": {"prediction": predicted_gender, "confidence": confidence_gender},
        "age": {"prediction": predicted_age}
    }
    # ---------------------------


    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    return render_template('result.html', results=results, image_file=image_base64)




if __name__ == '__main__':
  app.run(debug=True)