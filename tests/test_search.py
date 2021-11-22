import os
from unittest import TestCase

from adtools import ADTools, LdapCommands, objects


def ldap_add(file):
    file = os.path.join(os.path.dirname(__file__), file)
    return LdapCommands.ldap_add(file, 'localhost', 'cn=admin,dc=example,dc=com', 'test',
                                 continuous=True)


def ldap_delete(dn, recursive=False):
    return LdapCommands.ldap_delete(dn, 'localhost', 'cn=admin,dc=example,dc=com', 'test',
                                    recursive=recursive, continuous=True)


class SearchTest(TestCase):
    def setUp(self) -> None:
        self.adtools = ADTools()
        self.adtools.connect('localhost', 'cn=admin,dc=example,dc=com', 'test')
        ldap_delete('OU=Users,OU=adtools-test,OU=Test,DC=example,DC=com', recursive=True)
        ldap_add('test_data/ou_structure.ldif')
        ldap_add('test_data/users.ldif')
        ldap_add('test_data/groups.ldif')

    def test_get_user(self):
        user = self.adtools.get_user('CN=user2,OU=Users,OU=adtools-test,OU=Test,DC=example,DC=com')
        self.assertIsInstance(user, objects.User)

    def test_get_group(self):
        user = self.adtools.get_group('cn=group,ou=Users,ou=adtools-test,ou=Test,dc=example,dc=com')
        self.assertIsInstance(user, objects.Group)

    def test_has_member(self):
        user = self.adtools.get_user('CN=user2,OU=Users,OU=adtools-test,OU=Test,DC=example,DC=com')
        group = self.adtools.get_group(
            'cn=group,ou=Users,ou=adtools-test,ou=Test,dc=example,dc=com')
        self.assertIsInstance(group, objects.Group)
        self.assertTrue(group.has_member(user))

    def test_add_member(self):
        user = self.adtools.get_user('CN=user3,OU=Users,OU=adtools-test,OU=Test,DC=example,DC=com')
        group = self.adtools.get_group(
            'cn=group,ou=Users,ou=adtools-test,ou=Test,dc=example,dc=com')
        self.assertIsInstance(user, objects.User)
        self.assertIsInstance(group, objects.Group)
        self.assertFalse(group.has_member(user))
        group.add_member(user)
        self.assertTrue(group.has_member(user))
        self.assertTrue(user.has_group(group))

    def test_delete_member(self):
        user = self.adtools.get_user('CN=user2,OU=Users,OU=adtools-test,OU=Test,DC=example,DC=com')
        group = self.adtools.get_group(
            'cn=group,ou=Users,ou=adtools-test,ou=Test,dc=example,dc=com')
        self.assertIsInstance(user, objects.User)
        self.assertIsInstance(group, objects.Group)

        self.assertTrue(group.has_member(user))
        group.remove_member(user)
        self.assertFalse(group.has_member(user))
        self.assertFalse(user.has_group(group))

    def test_add_group(self):
        user = self.adtools.get_user('CN=user3,OU=Users,OU=adtools-test,OU=Test,DC=example,DC=com')
        group = self.adtools.get_group(
            'cn=group,ou=Users,ou=adtools-test,ou=Test,dc=example,dc=com')
        self.assertIsInstance(user, objects.User)
        self.assertIsInstance(group, objects.Group)
        self.assertFalse(group.has_member(user))
        user.add_group(group)
        self.assertTrue(group.has_member(user))
        self.assertTrue(user.has_group(group))

    def test_remove_group(self):
        user = self.adtools.get_user('CN=user2,OU=Users,OU=adtools-test,OU=Test,DC=example,DC=com')
        group = self.adtools.get_group(
            'cn=group,ou=Users,ou=adtools-test,ou=Test,dc=example,dc=com')
        self.assertIsInstance(user, objects.User)
        self.assertIsInstance(group, objects.Group)

        self.assertTrue(group.has_member(user))
        user.remove_group(group)
        self.assertFalse(group.has_member(user))
        self.assertFalse(user.has_group(group))
