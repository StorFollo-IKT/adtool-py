from ldap3 import Connection, SAFE_SYNC, Server, utils as ldap_utils

import exceptions
import utils


def check_result(result):
    if result['result'] == 32:
        raise exceptions.NoSuchObject(result)


class ADTools:
    conn = None

    def connect(self, dc, username, password, ldaps=False, port=None):
        server = Server(dc, port=port, use_ssl=ldaps)
        self.conn = Connection(
            server, username, password,
            client_strategy=SAFE_SYNC, auto_bind=True, raise_exceptions=True)

    def get_object(self, dn: str, attributes: list = None):
        base = utils.ou(dn)
        if attributes is None:
            attributes = []
        attributes.append('objectClass')

        dn = ldap_utils.conv.escape_filter_chars(dn)
        status, result, response, _ = self.conn.search(base,
                                                       '(distinguishedName=%s)' % dn, attributes=attributes)
        check_result(result)
        return response[0]['attributes']

    def group_members(self, group_dn):
        status, result, response, _ = self.conn.search(utils.ou(group_dn),
                                                       '(distinguishedName=%s)' % group_dn, attributes=['member'])

        return response[0]['attributes']['member']
