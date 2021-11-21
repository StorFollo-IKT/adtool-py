from ldap3.core.exceptions import LDAPAttributeOrValueExistsResult, LDAPNoSuchAttributeResult

from adtools import utils
from . import ADObject


class User(ADObject):
    groups: list

    def __init__(self, adtools, response):
        super().__init__(adtools, response)
        # self.groups = self['memberOf']
        self.groups = list(map(utils.uppercase_dn, self['memberOf']))

    def has_group(self, group_dn):
        # return group_dn in self.element['attributes']['memberOf']
        return group_dn in self.groups

    def remove_group(self, group_dn):
        try:
            self.adtools.remove_group_member(group_dn, self.dn)
        except LDAPNoSuchAttributeResult:
            pass
        self.groups.remove(group_dn)

    def add_group(self, group_dn):
        try:
            self.adtools.add_group_member(group_dn, self.dn)
        except LDAPAttributeOrValueExistsResult:
            pass
        self.groups.append(group_dn)

    def employee_id(self):
        return self.numeric('employeeID')
