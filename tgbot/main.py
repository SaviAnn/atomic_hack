import requests
import telebot
from io import BytesIO
import os, time

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

WEB_APP_URL = 'http://10.16.0.79:5003/process'
UPLOAD_FOLDER = 'C:\\Users\\ostarkov\\PycharmProjects\\flask\\uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@bot.message_handler(content_types=['photo'])

def handle_docs_photo(message):
    processing_message = bot.reply_to(message, "Изображения получены, идет обработка...")

    # Получаем изображение с максимальным разрешением
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Сохранение оригинального изображения локально
    original_filename = file_info.file_path.split('/')[-1]
    original_filepath = os.path.join(UPLOAD_FOLDER, original_filename)
    with open(original_filepath, 'wb') as new_file:
        new_file.write(downloaded_file)

    files = {'file': (original_filename, BytesIO(downloaded_file), 'image/jpeg')}
    response = requests.post(WEB_APP_URL, files=files)
    response_data = response.json()

    if response.status_code == 200:
        defect_type = response_data.get('defect_type')
        image_url = response_data.get('image_url')

        # Загружаем обработанное изображение по URL
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            # Создаем BytesIO объект из полученного изображения
            image_bytes = BytesIO(image_response.content)

            # Сохранение обработанного изображения локально с префиксом processed_
            processed_filename = f"processed______{original_filename}"
            processed_filepath = os.path.join(UPLOAD_FOLDER, processed_filename)
            with open(processed_filepath, 'wb') as processed_file:
                processed_file.write(image_response.content)

            # Отправка обработанного изображения пользователю
            bot.send_photo(message.chat.id, photo=image_bytes, caption=f"Тип дефекта: {defect_type}")
        else:
            bot.reply_to(message, "Не удалось загрузить обработанное изображение.")
    else:
        bot.reply_to(message, "Произошла ошибка при обработке изображения.")

    # Удаление сообщения об обработке
    bot.delete_message(chat_id=message.chat.id, message_id=processing_message.message_id)
def run_bot():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            time.sleep(1)  # Ожидание перед перезапуском
            continue





if __name__ == '__main__':
    run_bot()
