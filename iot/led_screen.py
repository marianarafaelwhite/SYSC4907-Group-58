"""
led_screen.py
"""
from sense_hat import SenseHat
import constants as c


class LedScreen:
    """
    Class to control the LED Screen
    """

    def __init__(self, sense_hat):
        """
        Initialize the LedScreen

        Parameters
        ----------
        sense_hat : SenseHat
        """
        self.__sense_hat = sense_hat
        self.__sense_hat.low_light = True

    def display_humidity(self, status):
        """
        """
        green = (0, 128, 0)
        red = (255, 0, 0)
        grey = (128, 128, 128)
        black = (0, 0, 0)

        colour = {c.SAFE: green,
                  c.WARNING: red}
        C = colour.get(status, grey)
        B = black

        display = [B, B, B, B, B, B, B, B,
                   B, B, B, B, B, B, B, B,
                   B, B, B, B, B, B, B, B,
                   B, B, B, B, B, B, B, B,
                   B, B, B, B, B, B, B, B,
                   B, C, C, B, B, B, B, B,
                   B, C, C, B, B, B, B, B,
                   B, B, B, B, B, B, B, B]

        pixel_list = self.__sense_hat.get_pixels()
        for i in range(0, len(pixel_list)):
            if pixel_list[i] != [0, 0, 0] and display[i] == black:
                display[i] = tuple(pixel_list[i])

        self.__sense_hat.set_pixels(display)

    def display_co2(self, status):
        """
        """
        green = (0, 128, 0)
        red = (255, 0, 0)
        grey = (128, 128, 128)
        black = (0, 0, 0)

        colour = {c.SAFE: green,
                  c.WARNING: red}
        C = colour.get(status, grey)
        B = black

        display = [B, B, B, B, B, B, B, B,
                   B, B, B, B, B, B, B, B,
                   B, B, B, B, B, B, B, B,
                   B, B, B, B, B, B, B, B,
                   B, B, B, B, B, B, B, B,
                   B, B, B, B, B, C, C, B,
                   B, B, B, B, B, C, C, B,
                   B, B, B, B, B, B, B, B]

        pixel_list = self.__sense_hat.get_pixels()
        for i in range(0, len(pixel_list)):
            if pixel_list[i] != [0, 0, 0] and display[i] == black:
                display[i] = tuple(pixel_list[i])

        self.__sense_hat.set_pixels(display)

    def clear(self):
        """
        Clears the screen
        """
        self.__sense_hat.clear()


if __name__ == '__main__':
    # LedScreen Manual Test
    sense = SenseHat()
    screen = LedScreen(sense)

    arrow_directions = ['left', 'right', 'up', 'down']
    update_screen = True
    count = 0

    try:
        while True:
            if update_screen:
                if count == 0:
                    screen.display_humidity(c.UNKNOWN)
                    screen.display_co2(c.UNKNOWN)
                elif count == 1:
                    screen.display_humidity(c.SAFE)
                elif count == 2:
                    screen.display_co2(c.SAFE)
                elif count == 3:
                    screen.display_humidity(c.WARNING)
                elif count == 4:
                    screen.display_co2(c.WARNING)
                    count = -1  # Reset

                count += 1
                update_screen = False

            events = sense.stick.get_events()
            for event in events:
                # Skip releases
                direction = event.direction
                action = event.action
                if action != 'released' and direction in arrow_directions:
                    update_screen = True
    except KeyboardInterrupt:
        screen.clear()
        print('Exiting due to keyboard interrupt')
