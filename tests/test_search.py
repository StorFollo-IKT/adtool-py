from unittest import TestCase

from adtools import ADTools, objects


class SearchTest(TestCase):
    def setUp(self) -> None:
        self.adtools = ADTools()
        self.adtools.connect('localhost', 'cn=admin,dc=example,dc=com', 'test')

    # def test_get_user(self):
    #     user = self.adtools.get_user('cn=user1,ou=Users,ou=adtools-test,ou=Test,dc=example,dc=com')
    #     self.assertIsInstance(user, objects.User)

    def test_get_group(self):
        user = self.adtools.get_group('cn=group,ou=Users,ou=adtools-test,ou=Test,dc=example,dc=com')
        self.assertIsInstance(user, objects.Group)