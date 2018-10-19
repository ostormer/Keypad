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
    
    #a3 - a5 om passord er rett, a4 hvis feil
    # verifisere login 
    def verify_login(self):
        if self.current_password == self.passcode_buffer:
            self.override_signal = "Y"
            self.twinkle_leds(dur, twinkle_dur)  # riktig passord, twinkle leds
        else:
            self.override_signal = "N"
            self.flash_leds(dur, flash_dur)  # skrev feil passord, flashe leds
    
    #a4
    def wrong_password_reset(self):
        #hvis det er feil passord, den er ikke logget inn
        #eller mens du skriver passord og trykker inn en # 
        pass
    
    #a6
    def reset_agent_attributes(self):
        #reset dur, lid, og muligens passcode buffer
        return
    
    
    
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
    #a2
    def add_to_passcode_buffer(self, sig: str):
        self.passcode_buffer += sig

    # obs! usikker på duration og hvordan det tolkes videre
    
    #a7
    def set_led_id(self, id: str):
        self.lid = int(id)
    #a8
    def begin_dur_entry(self):
        self.ldur = ""

    #a9
    def append_dur_digit(self, dur:str):
        self.ldur += dur

    #a10    
    def light_the_led(self):
        dur = int(self.ldur)
        self.light_one_led(self.lid, dur)

    def light_one_led(self, led_id, dur):
        self.ledboard.light_led(led_id, dur)  # ldur og lid

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
