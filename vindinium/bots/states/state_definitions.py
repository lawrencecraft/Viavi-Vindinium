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
            Transition(lambda t:
                       self.hero_health_is_less_than(30)(t) and
                       self.gold_is_greater_than(2)(t), lambda: GoToTavernState()),
            Transition(lambda t: self.hero_health_is_less_than(70)(t) and
                                 self.nearest_tavern_is()(t) == 1 and
                                 self.gold_is_greater_than(2)(t),
                       lambda: GoToTavernState()),
            Transition(lambda t: self.nearest_tavern_is()(t) > t.hero.life + 20,
                       lambda: GoToTavernState())
        ]

    def execute_move(self, bot_state):
        return self.go_to_nearest_mine(bot_state)

class CombatState(BaseState):
    def __init__(self):
        super(CombatState, self).__init__()
        self.state_name = "CombatState"
        self.transitions = []

    def execute_move(self, bot_state):
        pass

