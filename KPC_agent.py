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
        self.lid = None   # led id
        self.ldur = ""  # led duration

    # ready to receive password a1
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

    # a3 om passord er rett, a4 hvis feil
    # verifisere login
    def verify_login(self):
        if self.current_password == self.passcode_buffer:
            self.override_signal = "Y"
            self.twinkle_leds(2, 1./30)  # riktig passord, twinkle leds
            for i in range(10):
                self.light_one_led(0, 0.1)
                self.light_one_led(1, 0.1)
        else:
            self.override_signal = "N"
            self.flash_leds(2, 0.2)  # skrev feil passord, flashe leds
            for i in range(10):
                self.light_one_led(4, 0.1)
                self.light_one_led(5, 0.1)

    # a4, a5, a6
    def reset_agent_attributes(self):
        # reset dur, lid, og muligens passcode buffer
        self.override_signal = ""
        self.lid = None   # led id
        self.ldur = ""  # led duration
        self.passcode_buffer = ""

    # validere passordendring
    # a12
    def validate_passcode_change(self):
        if len(self.passcode_buffer) > 3 and self.passcode_buffer.isdigit():
            for i in range(10):
                self.light_one_led(0, 0.1)
                self.light_one_led(1, 0.1)
            self.change_password()
        else:
            for i in range(10):
                self.light_one_led(4, 0.1)
                self.light_one_led(5, 0.1)
            return "N"

    def change_password(self):
        f = open(self.password_file_name, 'w')
        f.write(self.passcode_buffer)
        f.close()
        self.current_password = self.passcode_buffer

    # adde en char til passcode_buffer
    # a2
    def add_to_passcode_buffer(self, sig: str):
        self.passcode_buffer += sig

    # obs! usikker på duration og hvordan det tolkes videre

    # a7
    def set_led_id(self, id: str):
        self.lid = int(id)
    # a8

    def begin_dur_entry(self):
        self.ldur = ""

    # a9
    def append_dur_digit(self, dur: str):
        self.ldur += dur

    # a10
    def light_selected_led(self):
        dur = int(self.ldur)
        self.light_one_led(self.lid, dur)

    def light_one_led(self, led_id, dur):
        self.ledboard.light_led(led_id, dur)  # ldur og lid

    def flash_leds(self, dur, flash_dur):
        self.ledboard.flash_all_leds(dur, flash_dur)

    def twinkle_leds(self, dur, twinkle_dur):
        self.ledboard.twinkle_all_leds(dur, twinkle_dur)

    #a14
    def exit_action(self):
        self.reset_agent_attributes()
        self.ledboard.power_down()

    def agent_do_action(self, action, sig):
        if action == "a1":
            print("Powering up")
            self.init_passcode_entry()
        elif action == "a2":
            print("Add %s to buffer" % sig)
            self.add_to_passcode_buffer(sig)
        elif action == "a3":
            print("Verifying login")
            self.verify_login()
        elif action in ["a4","a5","a6","a11"]:
            print("Reseting agent attributes")
            self.reset_agent_attributes()
        elif action == "a7":
            print("Setting led-id to %s" % sig)
            self.set_led_id(sig)
        elif action == "a8":
            self.begin_dur_entry()
        elif action == "a9":
            self.append_dur_digit(sig)
        elif action == "a10":
            self.light_selected_led()
        elif action == "a12":
            self.validate_passcode_change()
        elif action =="a14":
            self.exit_action()
        else:
            print("Rule %s is not recognised" % action)
