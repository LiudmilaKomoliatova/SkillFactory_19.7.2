"""Модуль 19"""
import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    """апи библиотека к веб приложению Pet Friends"""

    def __init__(self, url):
        self.base_url = url

    # This method allows to get API key which should be used for other API methods.
    def get_api_key(self, email: str, passwd: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключем пользователя, найденного по указанным email и паролем"""

        headers = field_remover({
            'email': email,
            'password': passwd,
        })
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    # This method allows to get the list of pets.
    def get_pets(self, auth_key: json, pet_filter: str = "") -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        со списком наденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
        либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
        собственных питомцев"""

        headers = {'auth_key': auth_key['key']}
        pet_filter = field_remover({'filter': pet_filter})

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=pet_filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    # This method allows to add information about new pet.
    def post_create_pet_simple(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        pet_field = field_remover({
            'name': name,
            'animal_type': animal_type,
            'age': age
        })
        data = MultipartEncoder(fields=pet_field)
        headers = {
            'auth_key': auth_key['key'],
            'Content-Type': data.content_type
        }
        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    # This method allows to add photo of a pet.
    def post_pets_set_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        pet_field = field_remover({
            'pet_id': pet_id,
            'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
        })
        data = MultipartEncoder(fields=pet_field)
        headers = {
            'auth_key': auth_key['key'],
            'Content-Type': data.content_type
        }
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    # This method allows to add information about new pet
    def post_pets(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""
        pet_field = field_remover({
            'name': name,
            'animal_type': animal_type,
            'age': age,
            'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
        })
        data = MultipartEncoder(fields=pet_field)
        headers = {
            'auth_key': auth_key['key'],
            'Content-Type': data.content_type
        }
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    # This method allows to delete information about pet from database.
    def delete_pets(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200"""
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    # This method allows to update information about pet.
    def put_pets(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер о обновлении данных питомуа по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлённыи данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = field_remover({
            'name': name,
            'age': age,
            'animal_type': animal_type
        })
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


# preparing wrong data
def field_remover(data):
    keys = [k for k in data.keys() if data[k] == 'None']
    for k in keys:
        data.pop(k)
    return data

