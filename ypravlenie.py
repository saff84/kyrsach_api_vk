from logic import data_file_encoding, init_vk, init_ya
import json

if __name__ == '__main__':
    # Инициализируем пользователя vk и запускаем парсинг фоток
    photos = init_vk()
    #Поправил логику работы с промежуточным файлом но в итоге сделал без промежуточного файла json
    # with open('photos.json', 'w') as file:
    #     json.dump(photos, file)

    # Преобразуем файл в файл с нужными названиями и адресами для скачивания
    spisok_photo = data_file_encoding(photos)

    # Инициализируем пользователя Яндекс диска и запускаем загрузку фоток в
    # нужную папку
    init_ya(spisok_photo)
