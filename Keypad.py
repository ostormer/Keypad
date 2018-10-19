# interface mellom keypad controller agent og keypad
import RPi.GPIO as GPIO
from time import sleep


class Keypad():
    # contains declarations of which RPI pins serve as inputs and outputs to the keypad code

    row_pin = [18, 23, 24, 25]
    colm_pin = [17, 27, 22]

    def rpi_setup(self):
        GPIO.setmode(GPIO.BCM)

        for pin in self.row_pin:
            GPIO.setup(pin, GPIO.OUT)
        for pin in self.colm_pin:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def poll_keypad(self):
        pins_to_sym = {
            (18, 17): "1",
            (18, 27): "2",
            (18, 22): "3",
            (23, 17): "4",
            (23, 27): "5",
            (23, 22): "6",
            (24, 17): "7",
            (24, 27): "8",
            (24, 22): "9",
            (25, 17): "*",
            (25, 27): "0",
            (25, 22): "#"
        }
        # må legge inn sleep her
        for row in self.row_pin:
            GPIO.output(row, GPIO.HIGH)
            sleep(0.1)  # wait to maybe let it turn on
            for colm in self.colm_pin:
                if(GPIO.INPUT(colm) == GPIO.HIGH):
                    GPIO.ouput(row, GPIO.LOW)
                    return pins_to_sym[(row, colm)]
            GPIO.ouptput(row, GPIO.LOW)

    def get_next_signal(self):
        while True:
            return self.poll_keypad()
