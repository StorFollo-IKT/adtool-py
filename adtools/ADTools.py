import re
from typing import Optional

import ldap3
from ldap3.core import exceptions as ldap_exceptions

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
            auto_bind=True, raise_exceptions=True)

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

    def _paginated_search(self, search_base, query, attributes=None, search_scope='SUBTREE'):
        elements = []
        self.conn.search(
                search_base=search_base,
                search_filter=query,
                search_scope=search_scope,
                attributes=attributes,
                paged_size=5)

        for element in self.conn.response:
            elements.append(self._find_object_class(element))
        cookie = self.conn.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
        while cookie:
            self.conn.search(
                    search_base=search_base,
                    search_filter=query,
                    search_scope=search_scope,
                    attributes=attributes,
                    paged_size=5,
                    paged_cookie=cookie)
            cookie = self.conn.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
            for element in self.conn.response:
                elements.append(self._find_object_class(element))
        return elements

    def search(self, search_base, query, attributes=None, search_scope='SUBTREE', pagination=False):
        if attributes is None:
            attributes = []
        attributes.append('objectClass')
        if pagination:
            return self._paginated_search(search_base, query, attributes, search_scope)

        self.conn.search(search_base, query,
                         attributes=attributes,
                         search_scope=search_scope)
        response = self.conn.response
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
        try:
            return self.conn.modify(group_dn, {'member': [(ldap3.MODIFY_ADD, [member_dn])]})
        except ldap_exceptions.LDAPEntryAlreadyExistsResult:
            pass

    def remove_groups(self, user_dn, groups):
        for group in groups:
            self.remove_group_member(group, user_dn)
