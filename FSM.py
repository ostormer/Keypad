# setting some methods that we will use

def all_symbols(symbol): return symbol is not None

def all_digits(symbol): return 48 <= ord(symbol) <= 57

def led_id(signal): return 48 <= ord(signal) <= 53




class FiniteStateMachine:

    def __init__(self):
        self.rule_list = []
        self.current_state = "s-init"
        self.current_action = "a0"
        self.current_symbol = "0"

        self.add_rule("s-init", "s-read", all_symbols, "a1")  # tar oss fra init til read via @

        self.add_rule("s-read1", "s-read1", all_digits, "a2")  # ber agenten appende passord tall
        self.add_rule("s-read1", "s-verify1", "*", "a3")  # ber agenten sjekke passord
        self.add_rule("s-read1", "s-init", all_symbols, "a4")  # sender oss tilbake til init ved "#"

        self.add_rule("s-verify1", "s-active", "Y", "a5")  # sender oss til s-active om passord er rett
        self.add_rule("s-verify1", "s-init", all_symbols(), "a4")  # sender oss til s-init om passord er feil

        self.add_rule(self.current_state, "s-logout", "#", "a6")  # etter s-active vil "#" alltid sende oss til logout

        self.add_rule("s-active", "s-led", led_id, "a7")  # sender oss til led id ved {0,5]
        self.add_rule("s-active", "s-read2", "*", "a1")  # samme passord prosess som ved oppstart
        self.add_rule("s-active", "s-active", all_symbols, "a6")  # ved tall høyere enn 5, gjør ingenting

        self.add_rule("s-led", "s-time", "*", "a8")  # må gjøre agenten klar til å ta inn tiden led skal lyse
        self.add_rule("s-led", "s-led", all_symbols, None)  # er i s-led, failer i å trykke "*", gjør ingenting

        self.add_rule("s-time", "s-time", all_digits, "a9")  # append tid digit i agent
        self.add_rule("s-time", "s-active", "*", "a10")  # execute LED greier i agenten

        self.add_rule("s-read2", "s-read2", all_digits, "a2")  # skriv inn riktig passord for å kunne endre
        self.add_rule("s-read2", "s-verify2", "*", "a3")  # veryfier på samme måte som tidligere

        self.add_rule("s-verify2", "s-read3", "Y", "a11")  # passord riktig, sender oss til "skriv nytt passord"
        self.add_rule("s-verify2", "s-active", all_symbols, "a6")  # passord feil, sender oss til s-active

        self.add_rule("s-read3", "s-read3", all_digits, "a12")  # append digit i nytt passord
        self.add_rule("s-read3", "s-active", "*", "a13")  # valider at nytt passord har 4 chars og sett som nytt passord







    # add new rule to FSM’s rule list.
    def add_rule(self, state1, state2, symbol, action):  # we assume that the specs of the rule are already defined
        self.rule_list.append(Rule(state1, state2, symbol, action))  # adds rule

    # query KPC agent for next signal.
    def get_next_signal(self):
        return None

    # go through rule list; fire first matching rule.
    def run_rules(self):

    # check whether rule conditions match current context.

    #uferdig kode:
    def apply_rule(self, rule):  # tar inn en regel
        correct_state = False  # brukes for å hjelpe returneringslogikken
        if self.current_state == rule.current_state:  # sammenligner regelens state med vår faktisk
            correct_state = True
        correct_symbol = False
        if isfunction(rule.signal):
            correct_symbol = rule.signal(self.current_symbol)
        elif isinstance(rule.signal, str):
            correct_symbol = (rule.signal == self.current_symbol)
        return correct_state and correct_symbol

    # use rule consequent to a) change FSM state, b) call agent action method.
    def fire_rule(self):
        return None

    # begin in FSM’s default init state; repeatedly call get next signal and run rules until the FSM enters its
    # default final state.
    def main_loop(self):
        self.current_state = "s-init"
        while True:
            self.current_symbol = self.agent.get_next_signal()
            self.run_rules()


class Rule:

    def __init__(self, state1, state2, symbol, action):
        self.state1 = state1
        self.state2 = state2
        self.symbol = symbol
        self.action = action

