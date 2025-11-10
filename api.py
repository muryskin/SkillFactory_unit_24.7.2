import pytest
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json

class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    @pytest.fixture()
    def get_api_key(self,email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса
        и результат  в формате JSON с уникальным ключом пользователя,
        найденным по указанным email и password."""
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result=""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str='') -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса
        и результат в формате JSON со списком найденных питомцев, совпадающих
        с фильтром. На данный момент фильтр может иметь либо пустое значение -
        получить список всех питомцев, либо 'my_pets' - получить список
        собственных питомцев."""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_pet_simple(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Метод делает запрос к API сервера и позволяет добавить информацию о новом питомце (без фото).
        Для добавления информации необходимо ввести имя name, тип животного animal_type, возраст age.
        Возвращает статус запроса и результат добавления в формате JSON."""
        data = {'name': name,'animal_type': animal_type,'age': age}
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """Метод делает запрос к API сервера и позволяет добавить информацию о новом питомце.
        Для добавления информации необходимо ввести имя name, тип животного animal_type, возраст age,
        название файла с изображением pet_photo.
        Возвращает статус запроса и результат добавления в формате JSON."""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def add_pet_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляем запрос к API сервера по указанному ID питомца и позволяет добавить
        фотографию. Возвращает статус запроса и данные питомца в формате JSON."""
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str) -> json:
        """Метод отправляет запрос к API сервера по указанному ID питомца и позволяет изменить
        информацию о нём. Возвращает статус запроса и обномленные данные питомца в формате JSON."""
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        headers = {'auth_key': auth_key['key']}

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet(self,auth_key: json, pet_id: str) -> json:
        """Метод отправляет запрос к API сервера по указанному ID питомца и позвляет удалить
        запись о нём. Возвращает статус запроса."""
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
