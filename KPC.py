# Main file for running the program
from FSM import *
from Keypad import *
from KPC_agent import *
from LedBoard import *


if __name__ == "__main__":
    fsm = FiniteStateMachine()
    fsm.main_loop()
