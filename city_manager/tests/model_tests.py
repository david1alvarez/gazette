from django.test import TestCase

from city_manager.models import City


class CityTestCase(TestCase):
    def setUp(self):
        City.objects.create(name="paris")
        City.objects.create(name="tokyo")

    def test_name(self):
        city = City.objects.get(name="paris")
        self.assertEqual(str(city), city.name)
