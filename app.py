from flask import Flask, render_template, request, url_for
import base64
import io

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

# Сторінка, яка обробляє завантажений файл і показує результат
@app.route('/analyze', methods=['POST'])
def analyze():
    # Перевіряємо, чи був файл завантажений
    if 'file' not in request.files:
        return "Помилка: файл не знайдено", 400
    
    file = request.files['file']

    # Перевіряємо, чи користувач вибрав файл
    if file.filename == '':
        return "Помилка: файл не вибрано", 400

    if file:
        # Читаємо байти зображення, щоб відобразити його на сторінці результатів
        image_bytes = file.read()
        # Кодуємо зображення в base64, щоб передати його в HTML
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # --- ІМІТАЦІЯ РОБОТИ AI ---
        # Тут, у майбутньому, буде реальний код для аналізу зображення
        # вашими трьома моделями. А поки що повертаємо "заглушку".
        results = {
            "race": {
                "prediction": "White",
                "confidence": "88.14%"
            },
            "gender": {
                "prediction": "Female",
                "confidence": "95.20%"
            },
            "age": {
                "prediction": 28
            }
        }
        # ---------------------------


        return render_template('result.html', results=results, image_file=image_base64)





if __name__ == '__main__':
  app.run(debug=True)