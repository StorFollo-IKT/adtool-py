from ldap3 import LEVEL

import objects


class OrganizationalUnit(objects.ADObject):
    def children(self):
        return self.adtools.search(self.dn, '(objectClass=organizationalUnit)', search_scope=LEVEL)
