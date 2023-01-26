import os
import unittest
from app.utils.env import get_from_env


class TestENV(unittest.TestCase):
    def test_get_from_env(self):
        env = get_from_env('ENV')
        self.assertIsNone(env)

        env = get_from_env('ENV', default='test')
        self.assertEqual(env, 'test')

        os.environ['ENV'] = 'test'
        env = get_from_env('ENV')
        self.assertEqual(env, 'test')
