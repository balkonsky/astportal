from backend.src.utils import validation_required, json_required, active_directory
from backend.src.models import User


def test():
    ad = active_directory.AD(
        host='172.20.2.173',
        port=389,
        username='dev-chat-svc',
        password='eew2Xuz9dovie5x',
        basedn='OU=Accounts,DC=humans,DC=dc',
        domain='',
        ssl=False,
        timeout=20)

    username = 'maksim.avramenko'
    if not ad.check_auth('humans\\' + username, 'aera2ote1Theong'):
        print('error user auth')
    else:
        print('success auth')

    profile = ad.get_user_profile(username,  [
        'displayName',
        'sAMAccountName',
        'mail',
        'mobile',
        'memberOf',
    ])
    print(profile)


if __name__ == '__main__':
    test()

