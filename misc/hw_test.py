#!/usr/bin/env python3
"""
Led

Re-factors LED hardware code from another project
"""
import RPi.GPIO as GPIO
from time import sleep
import logging
import constants as c

LED_OUTPUT_PIN = 21
BUTTON_INPUT_PIN = 20
TEST_TIME_SECS = 0.5
GPIO_WARNINGS_OFF = False
ON_STRING = 'ON'
OFF_STRING = 'OFF'
LED_OFF = 0
LED_ON = 1
BUTTON_IDLE = 0
BUTTON_PRESSED = 1
POLLING = True


class Led:
    """
    Class to represent Led

    Attributes
    ----------
    __pin : int
        BCM GPIO pin number
    __led_on : bool
        True if LED on

    Methods
    -------
    get_led_status()
        Returns the status of LED
    set_led_status(status)
        Sets the LED status
    invert_status()
        Inverts the status of the LED
    """

    def __init__(self, pin=LED_OUTPUT_PIN):
        """
        Initializes the Led

        Parameters
        ----------
        pin : int
            BCM GPIO pin number
        """
        self.__pin = pin
        self.__led_on = LED_OFF
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(GPIO_WARNINGS_OFF)
        GPIO.setup(self.__pin, GPIO.OUT)

    def get_status(self):
        """
        Returns
        -------
        self.__led_on : bool
            True if LED on
        """
        return self.__led_on

    def set_status(self, status):
        """
        Sets the LED status

        Parameters
        ----------
        status : bool
            True if LED on, False if LED off
        """
        output_gpio = None
        output_string = ''

        if status == LED_ON:
            output_gpio = GPIO.HIGH
            output_string = ON_STRING
        else:
            output_gpio = GPIO.LOW
            output_string = OFF_STRING

        GPIO.output(self.__pin, output_gpio)
        self.__led_on = status
        logging.debug('LED status updated to {}'.format(output_string))

    def invert_status(self):
        """
        Inverts the LED status
         - If LED status on, turn off LED
         - If LED status off, turn on LED

        Returns
        -------
        self.__led_on : bool
            True if LED on
        """
        self.set_status(not self.__led_on)
        return self.__led_on


class Button:
    """
    Class to represent the button

    Attributes
    ----------
    __pin : int
        BCM GPIO pin number

    Methods
    -------
    check_input()
        Checks if button was pressed
    """

    def __init__(self, pin=BUTTON_INPUT_PIN):
        """
        Initializes the button

        Parameters
        ----------
        pin : int
            BCM GPIO pin number
        """
        self.__pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(GPIO_WARNINGS_OFF)
        GPIO.setup(self.__pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def check_input(self):
        """
        Checks if the button has been pressed

        Returns
        -------
        bool
            True if button pressed
        """
        if GPIO.input(self.__pin):
            logging.debug("Button pressed")
            return BUTTON_PRESSED
        return BUTTON_IDLE


def test_hardware():
    """
    Tests LED and button
    """
    led = Led()
    button = Button()

    try:
        while POLLING:
            if button.check_input() == BUTTON_PRESSED:
                led.invert_status()
                sleep(TEST_TIME_SECS)
    except KeyboardInterrupt:
        logging.info('Exiting due to keyboard interrupt')
    except BaseException:
        logging.error('An error or exception occurred!')
    finally:
        led.set_status(LED_OFF)
        GPIO.cleanup()


if __name__ == '__main__':
    logging.basicConfig(format=c.LOGGING_FORMAT, level=logging.DEBUG)
    test_hardware()
