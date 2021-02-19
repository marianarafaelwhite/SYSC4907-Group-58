"""
test_hardware.py
"""
from iot.hardware import Hardware
from unittest import TestCase, main
from unittest.mock import patch, Mock


@patch('iot.hardware.Hardware.read_humidity')
@patch('iot.hardware.Hardware.read_co2')
class TestHardware(TestCase):

    def test_humidity(self, mock_co2, mock_humidity):
        """
        Test only running humidity sensor (HW Mocked)
        To ensure proper order of method calls
        """
        hw = Hardware(co2=False, humidity_sensor=Mock())
        hw.read_hardware()
        mock_humidity.assert_called_once_with()
        mock_co2.assert_not_called()

    def test_co2(self, mock_co2, mock_humidity):
        """
        Test only running CO2 sensor (HW Mocked)
        To ensure proper order of method calls
        """
        hw = Hardware(humidity=False, co2_sensor=Mock())
        hw.read_hardware()
        mock_humidity.assert_not_called()
        mock_co2.assert_called_once_with()

    def test_all_hardware(self, mock_co2, mock_humidity):
        """
        Test running all sensors (HW Mocked)
        To ensure proper order of method calls
        """
        hw = Hardware(humidity_sensor=Mock(), co2_sensor=Mock())
        hw.read_hardware()
        mock_humidity.assert_called_once_with()
        mock_co2.assert_called_once_with()


if __name__ == '__main__':
    main()
