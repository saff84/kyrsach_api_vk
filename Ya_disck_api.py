from pprint import pprint
import requests
import os

class YaUploader:
    def __init__(self, token: str):
        self.token = token
        self.host = 'https://cloud-api.yandex.net'

    def get_headers(self):
        return{
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
# Создаем нужную папку на Яндекс Диске
    def new_folder(self, file_path: str):
        new_folder = f'{self.host}/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': file_path}
        response = requests.put(new_folder, params = params, headers=headers)
        response.raise_for_status()
        if response.status_code == 201:
            print('Новая папка создана')

#Получаем ссылку для загрузки на яндекс диск
    def upload_link(self, file_path: str):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        url = f'{self.host}/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path':file_path, 'overwrite': True}
        response = requests.get(url, params = params, headers=headers)
        return response.json().get('href')

    # Загрузчик на Яндекс Диск
    def upload_file(self, path, file_name):
        up_link = self.upload_link(path)
        headers = self.get_headers()
        response = requests.put(up_link, data=open(file_name,'rb'), headers=headers)
        response.raise_for_status()
        if response.status_code == 201:
            print('Файл загружен')