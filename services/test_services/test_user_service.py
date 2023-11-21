import unittest

import models


class UserServiceEmptyOk:
    def get_all_users(self):
        return [models.User(id=1, firstName='aaa', lastname='aaa', email='aaa@aaa.aaa', role='student', password='aaa')]


class TestUserService(unittest.TestCase):
    def setUp(self) -> None:
        self.emptyok = UserServiceEmptyOk()
        self.notemptyok = UserServiceNotEmptyOk()

    def test_empty_ok(self):
        users = self.emptyok.get_all_users()
        self.assertEquals(users, [])


    def test_not_empty_ok(self):
        users = self.notemptyok.get_all_users()
        expected = models.User(id=1)
        self.assertEqual(users[0], expected)