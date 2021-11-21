from unittest import TestCase

from adtools import ADTools, objects


class SearchTest(TestCase):
    def setUp(self) -> None:
        self.adtools = ADTools()
        self.adtools.connect('localhost', 'cn=admin,dc=example,dc=com', 'test')

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
        self.assertTrue(user.has_group(group.dn))
