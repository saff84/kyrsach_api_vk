from vk_api import VkUser
from Ya_disck_api import YaUploader
import json
from pprint import pprint
import requests
import os
import time


if __name__ == '__main__':

    token_vk = "a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd"
    vk_client = VkUser(token_vk, '5.131')
    vk_id = input('Введите id ')  # 552934290

    # Получаем данные с vk и пишем в файл
    photos = vk_client.photos_get(vk_id)

    # Достаем из файла из вк нужные данные и формируем названия фотографий в
    # соответствии с требованиями
    with open('photos.json', "w", encoding="utf-8") as f:
        json.dump(photos, f)

    with open('photos.json') as json_file:
        data = json.load(json_file)
    # pprint(data)

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
    # token = ''

    token_ya = input('Введите токен для авторизации на Яндекс Диске: ')
    uploader = YaUploader(token_ya)
    upload_path = input('Введите название папки для загрузки: ')
    uploader.new_folder(upload_path)

    # Загружаем файлы с соответствющими названиями по url в ВК  в Яндекс Диск
    for photo in spisok_photo:
        file = f'{photo["file_name"]}'
        url = f'{photo["url"]}'
        # p_bar =
        print(f'Загружаю файл {file} в папку {upload_path}')
        result = uploader.upload_file(f'{upload_path}/{file}', url)

    print('Загрузка завершена')
