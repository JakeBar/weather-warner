from django.test import TestCase


class SimpleTestCase(TestCase):
    def test_assert_hello_world(self):
        self.assertTrue(True)
