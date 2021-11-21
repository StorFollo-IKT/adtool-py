from adtools import utils
from . import ADObject, User


class Group(ADObject):
    members = []

    def __init__(self, adtools, response):
        super().__init__(adtools, response)
        self.members = list(map(utils.uppercase_dn, self['member']))

    def add_member(self, user: User):
        user.groups.append(self.dn)
        self.members.append(user.dn)
        self.adtools.add_group_member(self.dn, user.dn)

    def remove_member(self, user: User):
        self.adtools.remove_group_member(self.dn, user.dn)
        try:
            user.groups.remove(self.dn)
        except ValueError:
            pass
        self.members.remove(user.dn)

    def has_member(self, user: User):
        return utils.uppercase_dn(user.dn) in self.members
