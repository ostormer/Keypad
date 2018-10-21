# interface mellom keypad controller agent og keypad
import RPi.GPIO as GPIO
from time import sleep


class Keypad:
    # contains declarations of which RPI pins serve as inputs and outputs to the keypad code

    row_pin = [18, 23, 24, 25]
    colm_pin = [17, 27, 22]

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

    def __init__(self):
        self.rpi_setup()
        self.prev_sig = ""

    def rpi_setup(self):
        GPIO.setmode(GPIO.BCM)
        for pin in self.row_pin:
            GPIO.setup(pin, GPIO.OUT)
        for pin in self.colm_pin:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def poll_keypad(self):
        # maybe add sleep() here?
        for row in self.row_pin:
            GPIO.output(row, GPIO.HIGH)
            sleep(0.01)  # wait to maybe let it turn on
            for colm in self.colm_pin:
                if(GPIO.input(colm) == GPIO.HIGH):
                    GPIO.output(row, GPIO.LOW)
                    # set this sig as previous sig, used in falling edge det.
                    self.prev_sig = Keypad.pins_to_sym[(row, colm)]
                    return self.prev_sig

            GPIO.output(row, GPIO.LOW)

    def get_next_signal(self):
        pre_sig = self.poll_keypad()
        while pre_sig == self.prev_sig:
            # still pressing last button pressed, waiting for release
            pre_sig = self.poll_keypad()

        while True:
            sig = self.poll_keypad()
            if sig:
                return sig


# --------------- TESTING ----------------
if __name__ == "__main__":
    kp = Keypad()
    i = 0
    sig = ""
    while(sig != "#"):
        sig = kp.get_next_signal()
        print(sig, flush=True, end = "")

    print()

    GPIO.cleanup()
