from backend.src.utils import validation_required, json_required, active_directory
from backend.src.models import User
import json


def test():
    ad = active_directory.AD(
        host='s01dcspb.ru.yotateam.com',
        port=389,
        username='opss_kitchen',
        password='XFV265Km',
        basedn='dc=ru,dc=yotateam,dc=com',
        domain='YOTARU',
        ssl=False,
        timeout=20)

    username = 'mavramenko'
    if not ad.check_auth(username, '5cEMtCxY'):
        print('error user auth')
    else:
        print('success auth')

    profile = ad.get_user_profile(username,  [
        'memberOf',
        'name',
        'fullName',
        'sAMAccountName',
        'mail',
        'mobile',
        'birthDate',
        'extensionAttribute8',
        'description',
        'department',
        'division',
        'inDate',
        'vkID'
    ])
    print(profile)
    return profile


def fill(profile_data):
    """ Парсит сырые данные из AD и заполняет модель """

    def safe_key(data, key, default='-'):
        """
            Возвращает из словаря ключ или default
            Сделано для обхода KeyError
        """
        try:
            if isinstance(data[key], list):
                return data[key][0]
            return data[key]
        except:
            return default
    json_data = json.loads(profile_data['data'][0])['attributes']
    print(json_data)


if __name__ == '__main__':
    fill(test())

