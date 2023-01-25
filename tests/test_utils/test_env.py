import unittest
from app.utils.env import get_from_env


class TestENV(unittest.TestCase):
    def test_get_from_env(self):
        env = get_from_env('ENV')
        self.assertIsNone(env)

        env = get_from_env('ENV', default='test')
        self.assertEqual(env, 'test')
