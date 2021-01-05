import re
import base64

from ldap3 import Server, Connection, RESTARTABLE, SUBTREE, ALL


class AD(object):
    """
    Active Directory

    :param str host: адрес сервера
    :param int port: порт сервера
    :param str username: имя сервисной учетной записи
    :param str password: пароль сервисной учетной записи
    :param str basedn: корень дерева (DIT), где будет выполняться поиск
    :param str domain: домен Active Directory
    :param bool ssl: использовать ли SSL при подключении
    :param int timeout: таймаут на подключение/ожидание ответа
    """

    def __init__(
            self, host, port, username, password,
            basedn, domain, ssl=False, timeout=10):

        self.basedn = basedn
        self.domain = domain
        self.timeout = timeout

        self.srv = self.get_server(host, port, ssl=ssl)
        self.con = self.get_connection(
            server=self.srv,  username=username, password=password)

    def get_server(self, host, port, ssl=False):
        return Server(
            host=host, port=port, use_ssl=ssl,
            get_info=ALL, connect_timeout=self.timeout)

    def get_connection(self, server, username, password):
        return Connection(
            server, user=f'{username}', password=password,
            client_strategy=RESTARTABLE, receive_timeout=self.timeout)

    def check_auth(self, username, password):
        """
        Авторизация пользователя по логину и паролю

        Выполняется попытка биндинга LDAP-соединения
        c кредами пользователя

        .. attention:: *YOTARU* и *@yotateam.com* в логине писать не надо

        :param str username: имя пользователя, например *ABogdanov*
        :param str password: пароль пользователя
        :return: результат биндинга, True или False
        :rtype: bool
        """
        connection = self.get_connection(
            server=self.srv, username=username, password=password)

        return connection.bind()

    def search_users(self, query, attributes=None):
        """
        Поиск пользователей

        :param str query: текст запроса
        :param list attributes: список нужных атрибутов, по-умолчанию -
            ["sAMAccountName", "memberOf"]
        :return: список профилей пользователей
        :rtype: list
        """

        if not attributes:
            attributes = ['sAMAccountName', 'memberOf']

        if '*' in attributes:
            raise RuntimeError('Wildcard forbidden in attributes list')

        if not self.con.bind():
            raise RuntimeError('AD service authentication failed')

        filter_query = f'''
            (
                &(objectClass=person)
                (|
                    (sAMAccountName=*{query}*)
                    (mobile=*{query}*)
                    (extensionAttribute8=*{query}*)
                    (fullName=*{query}*)
                )
            )
        '''
        search = self.con.search(
            search_base=self.basedn, search_filter=filter_query,
            attributes=attributes, search_scope=SUBTREE)

        result = []

        if not search or not self.con.entries:
            return result

        for entry in self.con.entries:
            person = Person(entry.entry_attributes_as_dict, attributes)
            result.append(person.to_dict)

        return result

    def get_user_profile(self, username, attributes=None):
        """
        Возвращает профиль пользователя

        :param str username: имя пользователя
        :param list attributes: список нужных атрибутов, по-умолчанию -
            ["sAMAccountName", "fullName", "mail", "mobile", "memberOf"]
        :return: профиль пользователя
        :rtype: dict
        """

        if not attributes:
            attributes = [
                'sAMAccountName', 'fullName',
                'mail', 'mobile', 'memberOf'
            ]

        if '*' in attributes:
            raise RuntimeError('Wildcard forbidden in attributes list')

        if not self.con.bind():
            raise RuntimeError('AD service authentication failed')

        filter_query = f'(&(objectClass=user)(sAMAccountName={username}))'
        search = self.con.search(
            search_base=self.basedn, search_filter=filter_query,
            attributes=attributes, search_scope=SUBTREE)

        if not search:
            raise RuntimeError('AD search failed')

        if len(self.con.entries) != 1:
            raise ValueError(f'Unexpected users: {self.con.entries}')

        entry = self.con.entries[0]
        person = Person(entry.entry_attributes_as_dict, attributes)

        return person.to_dict


class Person(object):
    """Person - парсит данные из AD и агрегирует их в профиль пользователя"""

    def __init__(self, entry: dict, attributes: list):
        self.ad = []
        self.ctx = []
        self._attributes = [attr for attr in attributes if attr in entry]
        self._parse_attr(entry)

    def _parse_attr(self, entry):
        for attr in self._attributes:
            if attr == 'memberOf':
                self._parse_groups(entry[attr])
                continue

            if attr == 'thumbnailPhoto' and entry[attr]:
                image = base64.b64encode(entry[attr][0])
                setattr(self, attr, image.decode('utf8'))
                continue

            if entry[attr]:
                setattr(self, attr, entry[attr][0])
            else:
                setattr(self, attr, str())

    def _parse_groups(self, groups: list):
        rex = re.compile(r'^CN=(.+?),\w+')
        for groupname in groups:
            search = rex.search(groupname)
            if search:
                if 'OU=SSLVPN' in groupname:
                    self.ctx.append(search.group(1))
                else:
                    self.ad.append(search.group(1))

    @property
    def groups(self):
        return dict(ad=self.ad, ctx=self.ctx)

    @property
    def to_dict(self):
        result = {}
        for attr in self._attributes:
            if attr == 'memberOf':
                result['groups'] = self.groups.copy()
                continue

            result[attr] = getattr(self, attr, str())

        return result
