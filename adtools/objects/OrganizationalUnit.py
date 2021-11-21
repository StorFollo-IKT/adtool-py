from ldap3 import LEVEL

from . import ADObject


class OrganizationalUnit(ADObject):
    def children(self):
        return self.adtools.search(self.dn, '(objectClass=organizationalUnit)', search_scope=LEVEL)
