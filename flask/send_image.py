import requests
import os
from urllib.parse import urljoin
from flask import url_for

server_url='http://localhost:5003/process'

def send_image_cnn(filepaths, server_url=server_url, save_path='uploads'):
    results = []
    # Убедитесь, что папка для сохранения существует
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for filepath in filepaths:
        filename = os.path.basename(filepath)
        print(filename)
        local_save_path = os.path.join(save_path, filename)

        with open(filepath, 'rb') as file:
            # Сохраняем файл локально
            # with open(local_save_path, 'wb') as local_file:
            #     local_file.write(file.read())

            # Переоткрываем файл для отправки
            with open(local_save_path, 'rb') as file_to_send:
                files = {'file': (filename, file_to_send)}
                # Отправляем файл в другое приложение Flask
                response = requests.post(server_url, files=files)
                print(files)
                if response.status_code == 200:
                    # Преобразуем ответ в JSON
                    data = response.json()




                    # Если в ответе есть URL изображения, загружаем изображение
                    if 'image_url' in data:
                        image_url = data['image_url']
                        print(image_url)
                        # Загрузка изображения по URL и сохранение его локально
                        image_response = requests.get(image_url)

                        if image_response.status_code == 200:
                            image_save_path = os.path.join(save_path, 'processed______' + filename)
                            with open(image_save_path, 'wb') as image_file:
                                image_file.write(image_response.content)
                            # Обновляем URL в данных на локальный путь
                            data['local_image_url'] = 'uploads/'+'processed______' + filename
                    results.append(data)
                    # Добавляем полученные данные в результаты
                    print(results,'res')
                else:
                    print(f'Ошибка при обработке файла {filepath}: {response.status_code}')

    return results