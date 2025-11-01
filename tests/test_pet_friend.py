import os

from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что запрос API ключа возвращает статус 200 и в результате содержится key."""

    # Отправляем запрос и сохраняем полученные код статуса в status, а текст ответа в result.
    status, result =  pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert "key" in result

def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем, что запрос всех питомцев возвращает не пустой список.
    Доступное значение параметра filter - 'my_pets' или ''."""

    # Получаем API ключ и сохраняем его в переменную auth_key.
    _, auth_key=pf.get_api_key(valid_email, valid_password)

    # Используя ключ запрашиваем список всех питомцев.
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверяем, что список не пустой
    assert status == 200
    assert len(result['pets']) > 0

def test_post_new_pet_without_photo(name='Kit', animal_type='Fish', age='2'):
    """Проверяем, что можно добавить питомца с корректыми данными, но без фотографии."""

    # Получаем API ключ и сохраняем его в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['age'] == age
    assert result['animal_type'] == animal_type
    assert result['name'] == name

def test_add_photo_to_pet(pet_photo = 'images/fish.jpg'):
    # Получаем API ключ и сохраняем его в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo.
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем список своих питомцев.
    _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')

    # Если список не пустой, то пробуем добавить фото питомца.
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        # Проверяем статус ответа и соответствие заданным значениям.
        assert status == 200
    else:
        # Если список питомцев пуст, вызываем исключение с текстом о пустом списке.
        raise AssertionError('There is no my pets to update.')

def test_post_new_pet_with_photo(name='Kopatych', animal_type='Bear', age='8', pet_photo='images/bear.jpg'):
    """Проверяем, что можно добавить питомца с корректыми данными и фотографией."""

    # Получаем API ключ и сохраняем его в переменную auth_key.
    _, auth_key=pf.get_api_key(valid_email, valid_password)

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo.
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['age'] == age
    assert result['animal_type'] == animal_type
    assert result['name'] == name

def test_update_pet_info(name='Krosh', animal_type='Hare', age='0'):
    """Проверяем возможность изменения информации о питомце."""

    # Получаем API ключ и сохраняем его в переменную auth_key.
    _, auth_key=pf.get_api_key(valid_email, valid_password)

    # Получаем список своих питомцев.
    _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')

    # Если список не пустой, то пробуем обновить имя, тип и возраст питомца.
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем статус ответа и соответвтсие заданным значениям.
        assert status == 200
        assert result['age'] == age
        assert result['animal_type'] == animal_type
        assert result['name'] == name
    else:
        # Если список питомцев пуст, вызываем исключение с текстом о пустом списке.
        raise AssertionError('There is no my pets to update.')

def test_delete_pet():
    """Проверяем возможность удаления питомца."""

    # Получаем API ключ и сохраняем его в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем список своих питомцев.
    _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')

    # Проверяем, если список питомцев пустой, то добавляем нового питомца
    # и снова вызываем список питомцев.

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Kit', 'Fish', '2', 'tests/images/fish.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')

    # Берём ID первого питомца и отправляем запрос на удаление.
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Запрашиваем список своих питомцев.
    _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')

    # Проверяем статус ответа и отсутствие ID удалённого питомца в списке.
    assert status == 200
    assert pet_id not in my_pets['pets']

# как будет реагировать тестируемое приложение, если мы в параметрах передадим
# слишком большое значение или вообще его не передадим? Что будет, если мы укажем
# неверный ключ авторизации и так далее?

# Подумать над вариантами тест-кейсов и написать ещё 10 различных тестов для данного REST API-интерфейса.

# 1. Отрицательное значение возраста                                            - при добавлении и изменении
# 2. Пустое значение имени, 3. типа животного или 4. возраста                   - при добавлении и изменении
# Недопустимые символы в имени, типе животного или возрасте:
#     5. isnumeric для возраста                                                 - при добавлении и изменении
#     6. isalpha для имени и 7. типа животного                                  - при добавлении и изменении
# 8. Неверный ключ авторизации для теста
# 9. Слишком большое количество символов для имени и 10. для типа животного     - при добавлении и изменении
# 11. Неверный логин и 12. пароль
# 13. Неверный фильтр для получения списка животных