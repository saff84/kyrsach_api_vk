import json
from Ya_disck_api import YaUploader
from vk_api import VkUser
import configparser

if __name__ == '__main__':
    #Вытаскиваем токен для Vk из settings.ini
    config_vk = configparser.ConfigParser()
    config_vk.read("settings.ini")
    token_vk = config_vk["vk"]["token"]

    vk_client = VkUser(token_vk, '5.131')
    vk_id = input('Введите id или коротке имя пользователя: ')  # 552934290
    vk_photos_count = int(input('Введите кол-во скачиваемых фотографий '))

    #Проверяем пришло id или screen_name
    if vk_id.isnumeric():
        photos = vk_client.photos_get(vk_id, vk_photos_count) # Получаем данные с vk и пишем в файл
    else:
        screen_name = vk_client.user_get(vk_id) # вытаскиваем id по screen_name
        photos = vk_client.photos_get(screen_name, vk_photos_count) # Получаем данные с vk и пишем в файл

    # Достаем из файла из вк нужные данные и формируем названия фотографий в соответствии с требованиями
    with open('photos.json', "w", encoding="utf-8") as f:
        json.dump(photos, f)

    with open('photos.json') as json_file:
        data = json.load(json_file)

    # формируем список с нужными данными из vk
    spisok_photo = []
    for photo in data:
        if str(photo['likes']['count']) + \
                ".jpg" in list(map(lambda x: x['file_name'], spisok_photo)):
            spisok_photo.append({"file_name": str(photo['likes']['count']) + "_" + str(photo['date']) + ".jpg", "size":
                                 photo['sizes'][photo['sizes'].index(max(photo['sizes'], key=lambda s: s['height'] * s['width']))][
                'type'], 'url': photo['sizes'][
                photo['sizes'].index(max(photo['sizes'], key=lambda s: s['height'] * s['width']))]['url']})
        else:
            spisok_photo.append({"file_name": str(photo['likes']['count']) + ".jpg", "size":
                                 photo['sizes'][photo['sizes'].index(max(photo['sizes'], key=lambda s: s['height'] * s['width']))][
                'type'], 'url': photo['sizes'][
                photo['sizes'].index(max(photo['sizes'], key=lambda s: s['height'] * s['width']))]['url']})

    #Вытаскиваем токен для Yandex из settings.ini - ток там пусто)
    # config_ya = configparser.ConfigParser()
    # config_ya.read("settings.ini")
    # token_ya = config_ya["Yandex"]["token"]


    token_ya = input('Введите токен для авторизации на Яндекс Диске: ')
    uploader = YaUploader(token_ya)
    upload_path = input('Введите название папки для загрузки: ')
    uploader.new_folder(upload_path)

    # Загружаем файлы с соответствющими названиями по url в ВК  в Яндекс Диск
    for photo in spisok_photo:
        file = f'{photo["file_name"]}'
        url = f'{photo["url"]}'
        print(f'Загружаю файл {file} в папку {upload_path}')
        result = uploader.upload_file(f'{upload_path}/{file}', url)

    print('Загрузка завершена')
