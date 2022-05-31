from logic import data_file_encoding, init_vk, init_ya

if __name__ == '__main__':
    # Инициализируем пользователя vk и запускаем парсинг фоток
    photos = init_vk()

    # Преобразуем файл в файл с нужными названиями и адресами для скачивания
    spisok_photo = data_file_encoding()

    # Инициализируем пользователя Яндекс диска и запускаем загрузку фоток в
    # нужную папку
    init_ya(spisok_photo)
