import os

from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


def test_update_pet_with_negative_age(age='-1'):
    """1. Проверяем возможность добавления отрицательного числа в возраст.
    Данная возможность должна отстутствовать и вызывать ошибку."""

    # Получаем API ключ и сохраняем его в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем список своих питомцев.
    _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')

    # Проверяем, если список питомцев пустой, то добавляем нового питомца
    # и снова вызываем список питомцев.
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Kit', 'Fish', '2', 'tests/images/fish.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')

    # Пробуем установить отрицательный возраст питомца.
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name='', animal_type='', age=age)
    # Проверяем, устанавливается ли отрицательный возраст.
    # Если устанвливается, то вызывается ошибка.
    if result['age'] == age or status == 200:
        raise AssertionError('Ошибка! Добавленно отрицательное значение возраста.')
    else:
        assert status != 200
        assert result['age'] != age

def test_add_new_pet_with_empty_param(name='', animal_type='', age=''):
    """2. Проверяем возможность добавления питомца с пустым полем в имени, типе и возрасте."""

    # Получаем API ключ и сохраняем его в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Проверяем, устанавливается ли пустые значения для имени, типа животного и возраста.
    # Если устанавливается, то вызывается ошибка.
    if status == 200:
        raise AssertionError(f'Ошибка! Добавленно пустое значение. name: {name}, animal_type: {animal_type}, age: {age}.')
    else:
        assert status != 200

def test_add_new_pet_with_non_numeric_age(name='Krosh', animal_type='Hare', age='12-!@#$_Alpha'):
    """3. Проверяем возможность добавления питомца с нецифровым возрастом."""

    # Получаем API ключ и сохраняем его в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Проверяем, устанавливается ли нецифровой возраст.
    # Если устанавливается, то вызывается ошибка.
    if status == 200:
        raise AssertionError(
            f'Ошибка! Добавленно нецифровое значение возраста. age: {age}.')
    else:
        assert status != 200

def test_add_new_pet_with_very_long_name(name=('Krosh '*20), animal_type='Hare', age='1'):
    """4. Проверяем возможность добавления питомца с очень длинным именем."""

    # Получаем API ключ и сохраняем его в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Проверяем, устанавливается ли очень длинное имя питомца.
    # Если устанавливается, то вызывается ошибка.
    if status == 200:
        raise AssertionError(
            f'Ошибка! Добавленно очень длинное имя питомца. name: {name}.')
    else:
        assert status != 200

def test_add_new_pet_with_very_long_type(name=('Krosh'), animal_type='Hare '*20, age='1'):
    """5. Проверяем возможность добавления питомца с очень длинным типом животного."""

    # Получаем API ключ и сохраняем его в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Проверяем, устанавливается ли очень длинный тип животного.
    # Если устанавливается, то вызывается ошибка.
    if status == 200:
        raise AssertionError(
            f'Ошибка! Добавленно очень длинный тип животного. animal_type: {animal_type}.')
    else:
        assert status != 200

def test_get_api_key_for_invalid_user(email="invalid@gmail.com", password="invalid_password"):
    """6. Проверяем для неверных значений email и password,
    что запрос API ключа не возвращает статус 200 и в результате не содержится key."""

    # Отправляем запрос и сохраняем полученные код статуса в status, а текст ответа в result.
    status, result =  pf.get_api_key(email, password)

    # Проверяем, что запрос не выполнен.
    if status == 200:
        raise AssertionError(
            f'Ошибка! API сервера принял неправильный email или пароль.')
    else:
        assert status != 200

def test_get_all_pets_with_invalid_key(filter=''):
    """7. Проверяем для неверного значения API ключа, что запрос всех питомцев не выполняется."""

    # Задаём заведомо неправильный API ключ.
    auth_key={'key':"123asd456fgh789"}

    # Используя ключ, запрашиваем список всех питомцев.
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверяем, что запрос не выполнен.
    if status == 200:
        raise AssertionError(
            f'Ошибка! Сервер принял неправильный API-ключ.')
    else:
        assert status != 200

def test_get_list_of_pets_with_invalid_filter(filter='my_friends_pets'):
    """8. Проверяем, что запрос питомцев с неправильным фильтром не выполняется.
    Доступное (правильное) значение параметра filter - 'my_pets' или ''."""

    # Получаем API ключ и сохраняем его в переменную auth_key.
    _, auth_key=pf.get_api_key(valid_email, valid_password)

    # Используя ключ запрашиваем список всех питомцев.
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверяем, что запрос не выполнен.
    if status == 200:
        raise AssertionError(
            f'Ошибка! Сервер принял не верный фильтр. filter: {filter}.')
    else:
        assert status != 200

def test_update_my_pet_info_with_empty_param(name='', animal_type='', age=''):
    """9. Проверяем возможность изменения имени, типа и возраста питомца на пустые."""

    # Получаем API ключ и сохраняем его в переменную auth_key.
    _, auth_key=pf.get_api_key(valid_email, valid_password)

    # Получаем список своих питомцев.
    _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')

    # Если список не пустой, то пробуем обновить имя, тип и возраст питомца.
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Записываем в переменные первоначальные значения
        # имени, типа животного и возраст для последующего сравнения.
        old_name = result['name']
        old_animal_type = result['animal_type']
        old_age = result['age']
        # Проверяем, устанавливается ли пустые значения для имени, типа животного и возраста.
        # Если устанавливается, то вызывается ошибка.
        if result['name']==name or result['animal_type']==animal_type or result['age']==age:
            raise AssertionError(
                f'Ошибка! Добавленно пустое значение. name: {name}, animal_type: {animal_type}, age: {age}.')
        else:
            # Иначе значения имени, типа животного и возраста не меняются.
            assert result['name']==old_name
            assert result['animal_type']==old_animal_type
            assert result['age']==old_age
    else:
        # Если список питомцев пуст, вызываем исключение с текстом о пустом списке.
        raise AssertionError('There is no my pets to update.')

    def test_update_my_pet_info_with_empty_param(name='', animal_type='', age=''):
        """9. Проверяем возможность изменения имени, типа и возраста питомца на пустые."""

        # Получаем API ключ и сохраняем его в переменную auth_key.
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Получаем список своих питомцев.
        _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')

        # Если список не пустой, то пробуем обновить имя, тип и возраст питомца.
        if len(my_pets['pets']) > 0:
            status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
            # Записываем в переменные первоначальные значения
            # имени, типа животного и возраст для последующего сравнения.
            old_name = result['name']
            old_animal_type = result['animal_type']
            old_age = result['age']
            # Проверяем, устанавливается ли пустые значения для имени, типа животного и возраста.
            # Если устанавливается, то вызывается ошибка.
            if result['name'] == name or result['animal_type'] == animal_type or result['age'] == age:
                raise AssertionError(
                    f'Ошибка! Добавленно пустое значение. name: {name}, animal_type: {animal_type}, age: {age}.')
            else:
                # Иначе значения имени, типа животного и возраста не меняются.
                assert result['name'] == old_name
                assert result['animal_type'] == old_animal_type
                assert result['age'] == old_age
        else:
            # Если список питомцев пуст, вызываем исключение с текстом о пустом списке.
            raise AssertionError('There is no my pets to update.')

def test_update_any_pet_info(name='Ваше животное', animal_type='изменено другим', age='¯\_(ツ)_/¯'):
    """10. Проверяем возможность изменения имени, типа и возраста любого питомца на сайте.
    Перед тестом необходимо убедиться, что первым питомцем в списке не является свой питомец."""

    # Получаем API ключ и сохраняем его в переменную auth_key.
    _, auth_key=pf.get_api_key(valid_email, valid_password)

    # Получаем список всех питомцев.
    _, pets = pf.get_list_of_pets(auth_key, filter='')

    # Пробуем изменить имя, тип и возраст чужого питомца.
    status, result = pf.update_pet_info(auth_key, pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем, получается ли изменить параметры чужого питомца.
    # Если получается, то вызывается ошибка.
    if result['name']==name or result['animal_type']==animal_type or result['age']==age:
        raise AssertionError(
            f'Ошибка! Были изменены параметры чужого питомца. name: {name}, animal_type: {animal_type}, age: {age}.')
    else:
        assert status != 200
