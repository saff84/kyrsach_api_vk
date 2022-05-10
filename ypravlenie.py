from vk_api import VkUser
from Ya_disck_api import YaUploader
import json
from pprint import pprint
import requests
import os
import time

name_directory = input('Введите название новой папки для загрузки фотографий: ')
if not os.path.isdir(name_directory):
     os.mkdir(name_directory)
     print(f'Папка {name_directory} создана')
else:
    print('Такая папка уже существует')
token = "a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd"
vk_client = VkUser(token, '5.131')
vk_id = int(input('Введите id ')) #552934290
# time.sleep(3)
#Получаем данные с vk и пишем в файл
photos = vk_client.photos_get(vk_id)
with open('photos.json', "w", encoding="utf-8") as f:
    json.dump(photos, f)

#Достаем из файла из вк нужные данные и формируем названия фотографий в соответствии с требованиями
with open('photos.json') as json_file:
    data = json.load(json_file)
# pprint(data)
spisok_photo = []
for photo in data:
    if  str(photo['likes']['count']) + ".jpg" in list(map(lambda x: x['file_name'], spisok_photo)):
        spisok_photo.append({"file_name": str(photo['likes']['count'])+ "_" + str(photo['date']) + ".jpg","size":photo['sizes'][-1]['type'],'url':photo['sizes'][-1]['url']})
    else:
        spisok_photo.append({"file_name": str(photo['likes']['count']) + ".jpg", "size": photo['sizes'][-1]['type'],
                         'url': photo['sizes'][-1]['url']})
# pprint(spisok_photo)

#Загружаем файлы с соответствющими названиями в отдельную папку на компьютер
for photo in spisok_photo:
    response = requests.get(photo['url'])
    filename = f'{photo["file_name"]}'
    if response.status_code == 200:
        with open(f'{name_directory}/{filename}',"wb") as f:
            f.write(response.content)

if __name__ == '__main__':
    # token = 'AQAAAAAPDYswAADLW-cnxjt4pkdRvcDsCQp3qMI'
    token = input('Введите токен для авторизации на Яндекс Диске: ')
    uploader = YaUploader(token)
    upload_path = input('Введите название папки для загрузки: ')
    uploader.new_folder(upload_path)

    for photo in spisok_photo:
        file = f'{name_directory}/{photo["file_name"]}'
        path_to_file = f'{os.path.split(file)[1]}'
        #p_bar =
        print(f'Загружаю файл {path_to_file} в папку {upload_path}')
        result = uploader.upload_file(f'{upload_path}/{os.path.split(file)[1]}',file)
    print('Загрузка завершена')
