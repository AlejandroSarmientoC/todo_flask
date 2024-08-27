import unittest
from config import Config, TestConfig

class ConfigTestCase(unittest.TestCase):

    def test_default_config(self):
        # Verifica los valores predeterminados en Config
        config = Config()
        self.assertEqual(config.SECRET_KEY, 'you-will-never-guess')
        self.assertEqual(config.MONGO_URI, 'mongodb://127.0.0.1:27017/todo_app')

    def test_test_config(self):
        # Verifica los valores en TestConfig
        test_config = TestConfig()
        self.assertTrue(test_config.TESTING)
        self.assertEqual(test_config.SECRET_KEY, 'you-will-never-guess')
        self.assertEqual(test_config.MONGO_URI, 'mongodb://127.0.0.1:27017/todo_app')

if __name__ == '__main__':
    unittest.main()