import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)


class Ledboard:
    """Running the led board, controlling the lights"""
    p0, p1, p2 = 5, 6, 13

    led_pins = {
        0: (6, 5, 13),
        1: (5, 6, 13),
        2: (13, 5, 6),
        3: (5, 13, 6),
        4: (13, 6, 5),
        5: (6, 13, 5)
    }

    def setup(self):
        pass

    def set_pin(self, pin, pin_state):
        """pin_state: 0 for LOW, 1 for HIGH, -1 for IN (disabled)"""
        if pin_state == -1:
            GPIO.setup(pin, GPIO.IN)
        else:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, pin_state)

    def light_led(self, led_id, led_dur):
        (hi, lo, dis) = Ledboard.led_pins[led_id]

        self.set_pin(hi, 1)
        self.set_pin(lo, 0)
        self.set_pin(dis, -1)

        time.sleep(led_dur)
        self.set_pin(hi, 0)
        self.set_pin(lo, 0)
        self.set_pin(dis, 0)

    def flash_all_leds(self, dur, flash_dur):
        t0 = time.time()
        on_time = t0
        while(time.time() - t0 < dur):
            if time.time() - on_time < flash_dur:
                for i in range(6):
                    (hi, lo, dis) = Ledboard.led_pins[i]
                    self.set_pin(hi, 1)
                    self.set_pin(lo, 0)
                    self.set_pin(dis, -1)
            else:  # Time to turn off between flashes
                self.set_pin(5, 0)
                self.set_pin(6, 0)
                self.set_pin(13, 0)
                time.sleep(flash_dur)
                on_time = time.time()
        self.set_pin(hi, 0)
        self.set_pin(lo, 0)
        self.set_pin(dis, 0)

    def twinkle_all_leds(self, dur, twinkle_dur):
        t0 = time.time()
        while(time.time() - t0 < dur):
            for i in range(6):
                self.light_led(i, twinkle_dur)

    def power_up(self):
        self.flash_all_leds(2, 0.4)
        self.twinkle_all_leds(2, 0.17)

    def power_down(self):
        self.twinkle_all_leds(2.5, 1 / 3)
        self.flash_all_leds(1.5, 0.2)


# -------------------------- TESTING -----------------------------
if __name__ == "__main__":
    lb = Ledboard()
    t0 = time.time()

    time.sleep(1)
    lb.flash_all_leds(5, 0.25)
    lb.twinkle_all_leds(5, 1./24)

    GPIO.cleanup()
