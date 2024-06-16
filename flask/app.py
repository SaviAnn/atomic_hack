from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.utils import secure_filename
import os

from send_image import send_image_cnn

app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Убедитесь, что папка для загрузки существует
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    # try:
    #     for i in os.listdir('temp'):
    #         print(i)
    #         os.remove('temp/'+i)
    # except:pass
    if request.method == 'POST':
        try:

            print(request.files.getlist('file'))
            files = request.files.getlist('file')  # Получаем список файлов
            processed_files_results = []  # Список для хранения результатов
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        print(type(filepath))
                        file.save(filepath)

                        # Обработка файла
                        result = send_image_cnn([filepath])  # Отправляем путь файла
                        processed_files_results.extend(result)  # Добавляем результаты в список
                    else:
                        flash('Недопустимый формат файла: ' + filename)
                else:
                    flash('Файл не был загружен или не выбран: ' + filename)
        except:return render_template('index.html')

        # Сохраняем результаты обработки всех файлов в сессии
        session['processed_files'] = processed_files_results
        return redirect(url_for('success'))

    return render_template('index.html')
@app.route('/success')
def success():
    # Получаем обработанные данные из сессии
    processed_files = session.get('processed_files', [])
    return render_template('success.html', processed_files=processed_files)


@app.route('/store')
def store():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    original_images = [file for file in files if not file.startswith('processed______')]
    images = {}
    for image in original_images:
        processed_image = f'processed______{image}'
        if processed_image in files:
            images[image] = processed_image
        else:
            images[image] = None

    return render_template('store.html', images=images)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Предоставляем доступ к загруженным файлам
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/remove-file/<filename>', methods=['POST'])
def remove_file(filename):
    # Удаление файла из сессии и файловой системы
    if 'processed_files' in session:
        # Обновляем информацию в сессии
        session['processed_files'] = [f for f in session['processed_files'] if f.get('image_name') != filename]
        print(session['processed_files'])
        # Удаляем файл из файловой системы
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)