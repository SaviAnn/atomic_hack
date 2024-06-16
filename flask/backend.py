from flask import Flask, request, jsonify, url_for, send_from_directory
import os

app = Flask(__name__)
from engine import process_image
# Проверяем и создаем папку temp при старте
if not os.path.exists('temp'):
    os.makedirs('temp')

# Добавляем route для отдачи файлов из папки temp
@app.route('/temp/<filename>')
def temp_file(filename):
    return send_from_directory('temp', filename)

@app.route('/process', methods=['POST'])
def process_file():
    file = request.files['file']
    filename = file.filename



    # Сохраняем файл
    temp_path = os.path.join('temp', filename)
    file.save(temp_path)




    process_image(temp_path)
    # Здесь обработка изображения


    # time.sleep(1)  # Имитация задержки в обработке
    with open('defect_type.txt','r')as file:
        defect_type=file.read()
    # Формируем ответ
    image_url = url_for('temp_file', filename=filename, _external=True)
    print(filename)
    print(defect_type+'123')
    response_data = {
        'image_url': image_url,
        'image_name': filename,
        'defect_type': defect_type
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)