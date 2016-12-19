from vindinium.bots.states import BaseState
from .transition import Transition


class GoToTavernState(BaseState):
    def __init__(self):
        super(GoToTavernState, self).__init__()
        self.state_name = "GoToTavernState"
        self.transitions = [
            Transition(self.hero_health_is_greater_than(80), lambda: GoToMineState())
        ]

    def execute_move(self, bot_state):
        return self.go_to_nearest_tavern(bot_state)


class GoToMineState(BaseState):
    def __init__(self):
        super(GoToMineState, self).__init__()
        self.state_name = "GoToMineState"
        self.transitions = [
            Transition(self.hero_health_is_less_than(20), lambda: GoToTavernState())
        ]

    def execute_move(self, bot_state):
        return self.go_to_nearest_mine(bot_state)
