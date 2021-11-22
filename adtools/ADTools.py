import re
from typing import Optional

import ldap3

from . import exceptions, objects, utils


def check_result(result):
    if result['result'] == 32:
        raise exceptions.NoSuchObject(result)


class ADTools:
    conn = None

    def __del__(self):
        if self.conn:
            self.conn.unbind()

    def _find_object_class(self, response):
        if 'objectClass' not in response['attributes']:
            raise ValueError('objectClass attribute not found, unable to detect class')
        object_class = response['attributes']['objectClass']

        if 'computer' in object_class:
            return objects.Computer(self, response)
        elif 'person' in object_class:
            return objects.User(self, response)
        elif 'group' in object_class:
            return objects.Group(self, response)
        elif 'organizationalUnit' in object_class:
            return objects.OrganizationalUnit(self, response)
        else:
            return objects.ADObject(self, response)

    def connect(self, dc, username, password, ldaps=False, port=None):
        server = ldap3.Server(dc, port=port, use_ssl=ldaps)
        self.conn = ldap3.Connection(
            server, username, password,
            client_strategy=ldap3.SAFE_SYNC, auto_bind=True, raise_exceptions=True)

    def get_object(self, dn: str, object_type: str, attributes=None):
        if attributes is None:
            attributes = []
        attributes.append('objectClass')

        dn = ldap3.utils.conv.escape_filter_chars(dn)
        query = '(&(objectClass=%s)(distinguishedName=%s))' % (object_type, dn)

        response = self.search(utils.ou(dn), query, attributes)
        if not response:
            return None

        return response[0]

    def search(self, search_base, query, attributes=None, search_scope='SUBTREE'):
        if attributes is None:
            attributes = []
        attributes.append('objectClass')
        status, result, response, _ = self.conn.search(search_base, query,
                                                       attributes=attributes,
                                                       search_scope=search_scope)
        check_result(result)
        if not response:
            return None

        elements = []
        for element in response:
            elements.append(self._find_object_class(element))

        return elements

    def get_user(self, dn, attributes=None) -> Optional[objects.User]:
        if attributes is None:
            attributes = []
        if 'memberOf' not in attributes:
            attributes.append('memberOf')

        matches = re.match(r'CN=(.+?),(OU=.+)', dn, flags=re.IGNORECASE)
        cn = matches.group(1)
        ou = matches.group(2)

        response = self.search(ou, '(cn=%s)' % cn, attributes, ldap3.LEVEL)
        if not response:
            return None

        return response[0]

    def get_group(self, dn, attributes=None) -> Optional[objects.Group]:
        if attributes is None:
            attributes = ['member']
        return self.get_object(dn, 'group', attributes)

    def group_members(self, group_dn):
        status, result, response, _ = self.conn.search(utils.ou(group_dn),
                                                       '(distinguishedName=%s)' % group_dn, attributes=['member'])

        return response[0]['attributes']['member']

    def remove_group_member(self, group_dn, member_dn):
        return self.conn.modify(group_dn, {'member': [(ldap3.MODIFY_DELETE, [member_dn])]})

    def add_group_member(self, group_dn, member_dn):
        return self.conn.modify(group_dn, {'member': [(ldap3.MODIFY_ADD, [member_dn])]})

    def remove_groups(self, user_dn, groups):
        for group in groups:
            self.remove_group_member(group, user_dn)
