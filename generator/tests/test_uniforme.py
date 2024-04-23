from django.test import TestCase

from generator.uniforme import Uniforme


class UniformeTestCase(TestCase):
    def test_uniforme(self):
        upper_limit = 20
        lower_limit = 8
        generator = Uniforme(lower_limit, upper_limit)

        for i in range(30):
            self.assertLess(generator.get_next_number(), upper_limit)
            self.assertGreater(generator.get_next_number(), lower_limit)
    
    def test_includes_limits(self):
        upper_limit = 1
        lower_limit = 1
        generator = Uniforme(lower_limit, upper_limit)
        self.assertEqual(generator.get_next_number(), upper_limit)

