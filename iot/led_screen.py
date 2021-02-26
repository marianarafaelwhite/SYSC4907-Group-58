"""
led_screen.py
"""
from sense_hat import SenseHat


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

    def display_safe(self):
        """
        Displays safe message on screen
        """
        G = (0, 128, 0)  # Green
        B = (0, 0, 0)   # Black

        display = [B, B, B, B, B, B, B, B,
                   B, B, B, B, B, B, B, G,
                   B, B, B, B, B, B, G, G,
                   B, B, B, B, B, G, G, B,
                   G, B, B, B, G, G, B, B,
                   G, G, B, G, G, B, B, B,
                   B, G, G, G, B, B, B, B,
                   B, B, G, B, B, B, B, B]
        self.__sense_hat.set_pixels(display)

    def display_warning(self):
        """
        Displays warning message on screen
        """
        Y = (255, 215, 0)   # Yellow (Gold)
        B = (0, 0, 0)       # Black

        display = [B, B, B, Y, B, B, B, B,
                   B, B, B, Y, B, B, B, B,
                   B, B, Y, B, Y, B, B, B,
                   B, B, Y, B, Y, B, B, B,
                   B, Y, Y, B, Y, Y, B, B,
                   B, Y, Y, Y, Y, Y, B, B,
                   Y, Y, Y, B, Y, Y, Y, B,
                   Y, Y, Y, Y, Y, Y, Y, B]
        self.__sense_hat.set_pixels(display)

    def display_unknown(self):
        """
        Displays unknown message on screen
        """
        G = (128, 128, 128)  # Grey
        B = (0, 0, 0)   # Black

        display = [B, B, B, G, B, B, B, B,
                   B, B, G, B, G, B, B, B,
                   B, G, B, B, B, G, B, B,
                   B, B, B, B, B, G, B, B,
                   B, B, B, G, G, G, B, B,
                   B, B, B, G, B, B, B, B,
                   B, B, B, B, B, B, B, B,
                   B, B, B, G, B, B, B, B]
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

    displays = [screen.display_unknown,
                screen.display_warning,
                screen.display_safe]
    arrow_directions = ['left', 'right', 'up', 'down']
    count = 0
    update_screen = True

    try:
        while True:
            if update_screen:
                displays[count % len(displays)]()
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
