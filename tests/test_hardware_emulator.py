"""
test_hardware_emulator.py
"""
from iot.hardware_emulator import HardwareEmulator
from unittest import TestCase, main
from unittest.mock import patch, Mock


@patch('iot.hardware_emulator.HardwareEmulator.generate_humidity')
@patch('iot.hardware_emulator.HardwareEmulator.generate_co2')
class TestHardwareEmulator(TestCase):

    def test_humidity(self, mock_co2, mock_humidity):
        """
        Test only running humidity sensor (HW Mocked)
        To ensure proper order of method calls
        """
        hw = HardwareEmulator(co2=False, hardware_id=123456789)
        hw.emulate_data()
        mock_humidity.assert_called_once_with()
        mock_co2.assert_not_called()

    def test_co2(self, mock_co2, mock_humidity):
        """
        Test only running CO2 sensor (HW Mocked)
        To ensure proper order of method calls
        """
        hw = HardwareEmulator(humidity=False, hardware_id=123456789)
        hw.emulate_data()
        mock_humidity.assert_not_called()
        mock_co2.assert_called_once_with()

    def test_all_hardware(self, mock_co2, mock_humidity):
        """
        Test running all sensors (HW Mocked)
        To ensure proper order of method calls
        """
        hw = HardwareEmulator(hardware_id=123456789)
        hw.emulate_data()
        mock_humidity.assert_called_once_with()
        mock_co2.assert_called_once_with()


if __name__ == '__main__':
    main()
