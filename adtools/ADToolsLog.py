import os
from datetime import datetime

from adtools import ADTools


class ADToolsLog(ADTools):
    debug = False

    def __init__(self, log_file_fp):
        self.fp = log_file_fp
        super(ADToolsLog, self).__init__()

    def log(self, message):
        date = datetime.now().strftime('%Y-%m-%d %H:%I:%S')
        self.fp.write('%s: %s%s' % (date, message, os.linesep))
        if self.debug:
            print(message)

    def remove_group_member(self, group_dn, member_dn):
        self.log('Remove %s from %s' % (member_dn, group_dn))
        return super().remove_group_member(group_dn, member_dn)

    def add_group_member(self, group_dn, member_dn):
        self.log('Add %s to group %s' % (member_dn, group_dn))
        return super().add_group_member(group_dn, member_dn)

    def remove_groups(self, user_dn, groups):
        self.log('Remove groups from %s: %s' % (user_dn, os.linesep.join(groups)))
