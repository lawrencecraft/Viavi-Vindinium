from vindinium.bots import BaseBot
from vindinium.bots.states.base_state import BaseState


class StateMachineBot(BaseBot):
    def __init__(self, base_state):
        """
        :type base_state: BaseState
        :param base_state:
        """
        self.current_state = base_state

    def move(self):
        current_name = self.current_state.state_name
        self.current_state = self.current_state.get_state(self)
        if current_name != self.current_state.state_name:
            print("Transitioned state: from " + current_name + " to " + self.current_state.state_name)
        return self.current_state.execute_move(self)
