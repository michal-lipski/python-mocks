import unittest

from mock import Mock, call

from pragmatists.snowmocks.SnowRescueService import SnowRescueService
from pragmatists.snowmocks.dependencies import PressService
from pragmatists.snowmocks.dependencies.SnowplowMalfunctioningException import SnowplowMulfunctioningException
from pragmatists.snowmocks.dependencies.WeatherForecastService import WeatherForecastService
from pragmatists.snowmocks.dependencies.MunicipalServices import MunicipalServices


class SnowRescueServiceTest(unittest.TestCase):

    def setUp(self):
        self.press_service = Mock(spec=PressService)
        self.municipal_services = Mock(spec=MunicipalServices)
        self.weather_forecast_service = Mock(spec=WeatherForecastService)
        self.service = SnowRescueService(self.weather_forecast_service, self.municipal_services, self.press_service)

    def test_send_snowplow_if_below_zero(self):
        self.weather_forecast_service.get_snow_fall_height_in_mm.return_value = -1
        self.service.check_forecast_and_rescue()

        self.municipal_services.send_sender.assert_called()

    def test_do_not_send_snowplow_if_zero_or_more(self):
        self.weather_forecast_service.get_snow_fall_height_in_mm.return_value = 0
        self.service.check_forecast_and_rescue()

        self.assertFalse(self.municipal_services.send_sender.called)

    def test_send_another_if_malfunctions(self):
        self.municipal_services.send_snowplow.side_effect = [SnowplowMulfunctioningException, None]
        self.weather_forecast_service.get_snow_fall_height_in_mm.return_value = -4
        self.service.check_forecast_and_rescue()

        self.assertEqual(2, self.municipal_services.send_snowplow.call_count)


if __name__ == '__main__':
    unittest.main()

