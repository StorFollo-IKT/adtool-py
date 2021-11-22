from ldap3.core.exceptions import LDAPAttributeOrValueExistsResult, LDAPNoSuchAttributeResult

from adtools import utils
from . import ADObject, Group


class User(ADObject):
    groups: list

    def __init__(self, adtools, response):
        super().__init__(adtools, response)
        self.groups = list(map(utils.uppercase_dn, self['memberOf']))

    def has_group(self, group: Group):
        return group.dn in self.groups

    def remove_group(self, group: Group):
        try:
            self.adtools.remove_group_member(group.dn, self.dn)
        except LDAPNoSuchAttributeResult:
            pass
        if group.dn in self.groups:
            self.groups.remove(group.dn)
        group.members.remove(self.dn)

    def add_group(self, group: Group):
        try:
            self.adtools.add_group_member(group.dn, self.dn)
        except LDAPAttributeOrValueExistsResult:
            pass
        self.groups.append(group.dn)
        group.members.append(self.dn)

    def employee_id(self):
        return self.numeric('employeeID')
