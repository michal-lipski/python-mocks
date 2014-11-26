import unittest
from mock import MagicMock
from pragmatists.snowmocks.dependencies.WeatherForecastService import WeatherForecastService


class SnowRescueServiceTest(unittest.TestCase):
    def test_i_can_mock(self):
        w = WeatherForecastService()
        w.get_snow_fall_height_in_mm = MagicMock()
        w.get_snow_fall_height_in_mm.return_value = 3
        self.assertEqual(3, w.get_snow_fall_height_in_mm())

if __name__ == '__main__':
    unittest.main()

