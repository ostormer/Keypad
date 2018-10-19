from LedBoard import*
from Keypad import*


class KPC_agent():
    def __init__(self):
        self.keypad = Keypad()
        self.ledboard = Ledboard()
        self.passcode_buffer = ""

        # filename to store the password, read initial password from this
        self.password_file_name = "password.txt"
        file = open(self.password_file_name, "r")
        self.current_password = file.read().strip()
        file.close()

        self.override_signal = ""
        self.lid = 0   # led id
        self.ldur = None  # led duration

    # ready to receive password
    def init_passcode_entry(self):
        self.passcode_buffer = ""
        self.ledboard.power_up()

    # hente neste signal
    def get_next_signal(self):
        # om override_signal ikke er tom, les inn neste signal
        if self.override_signal:
            signal = self.override_signal
            self.override_signal = ""
        else:
            signal = self.keypad.get_next_signal()

        return signal

    # verifisere login
    def verify_login(self):
        if self.current_password == self.passcode_buffer:
            self.override_signal = "Y"
            self.twinkle_leds(dur, twinkle_dur)  # riktig passord, twinkle leds
        else:
            self.override_signal = "N"
            self.flash_leds(dur, flash_dur)  # skrev feil passord, flashe leds

    # validere passordendring
    def validate_passcode_change(self):
        if len(self.passcode_buffer) > 3 and self.passcode_buffer.isdigit():
            f = open(self.password_file_name, 'w')
            f.write(self.passcode_buffer)
            f.close()
            self.current_password = self.passcode_buffer

            self.twinkle_leds(3, 0.1)
        else:
            self.flash_leds(3, 0.3)

    # adde en char til passcode_buffer
    def add_to_passcode_buffer(self, sig: str):
        self.passcode_buffer += sig

    # obs! usikker på duration og hvordan det tolkes videre
    def set_led_id(self, id: str):
        self.lid = int(id)

    def set_ldur(self, dur: str):
        self.ldur = int(dur)

    def light_one_led(self, led):
        self.ledboard.light_led(led)  # ldur og lid

    def flash_leds(self, dur, flash_dur):
        self.ledboard.flash_all_leds(dur, flash_dur)

    def twinkle_leds(self, dur, twinkle_dur):
        self.ledboard.twinkle_all_leds(dur, twinkle_dur)

    def exit_action(self):
        self.ledboard.power_down()
        self.passcode_buffer = ""
        self.lid = 0
        self.ldur = 0

    def states_to_action(self, sig):
        pass
