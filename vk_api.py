import json
from pprint import pprint
import requests
import os

class VkUser:
    url = 'https://api.vk.com/method/'
    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def photos_get(self, owner):
        photos_get_url = self.url + 'photos.get'
        album = int(input('''Введите индификатор альбома:\n
                         1 — фотографии со стены\n
                         2 — фотографии профиля\n'''))
        if album == 1:
            album_id = 'wall'
        else:
            album_id = 'profile'

        photos_get_params = {
            "owner_id": owner,
            "album_id": album_id,
            "size": "z",
            'extended': 1,
            'count': 300
        }
        req = requests.get(photos_get_url, params={**self.params, **photos_get_params}).json()
        return req['response']['items']

