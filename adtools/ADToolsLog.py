from adtools import ADTools


class ADToolsLog(ADTools):
    debug = False

    def log(self, message):
        if self.debug:  # TODO: Save messages to file
            print(message)

    def remove_group_member(self, group_dn, member_dn):
        self.log('Remove %s from %s' % (member_dn, group_dn))
        return super().remove_group_member(group_dn, member_dn)

    def add_group_member(self, group_dn, member_dn):
        self.log('Add %s to group %s' % (member_dn, group_dn))
        return super().add_group_member(group_dn, member_dn)
