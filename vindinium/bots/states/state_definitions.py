from vindinium.bots.states import BaseState
from .transition import Transition


class GoToTavernState(BaseState):
    def __init__(self, turns_stood_still=0):
        super(GoToTavernState, self).__init__()
        self.state_name = "GoToTavernState"
        self.turns_stood_still = turns_stood_still
        self.transitions = [
            Transition(lambda t: self.hero_health_is_greater_than(80)(t)
                       and self.nearest_neighbor(t) > 2, lambda: GoToMineState()),
            Transition(lambda t: self.turns_stood_still > 2, lambda: GoToMineState())
        ]

    def execute_move(self, bot_state):
        return self.go_to_nearest_tavern(bot_state)

    def construct(self):
        return GoToTavernState(self.turns_stood_still + 1)


class GoToMineState(BaseState):
    def __init__(self):
        super(GoToMineState, self).__init__()
        self.state_name = "GoToMineState"
        self.cached_result = None
        self.transitions = [
            Transition(self.hero_health_is_less_than(22),
                       lambda: GoToTavernState()),
            Transition(lambda t:
                       self.go_to_nearest_mine_wrapped(t)[1] + 20 > t.hero.life and
                       self.gold_is_greater_than(1)(t),
                       lambda: GoToTavernState()),
            Transition(lambda t: self.hero_health_is_less_than(70)(t) and
                                 self.nearest_tavern_is()(t) == 1 and
                                 self.gold_is_greater_than(1)(t),
                       lambda: GoToTavernState()),
            Transition(lambda t: self.my_projected_score(t) - self.get_highest_projected_score(t) > 50 and
                                 self.game_is_almost_over(t),
                       lambda: DefensiveState())
        ]

    def execute_move(self, bot_state):
        return self.go_to_nearest_mine_wrapped(bot_state)[0]

    def go_to_nearest_mine_wrapped(self, bot_state):
        if self.cached_result:
            return self.cached_result
        result = self.go_to_nearest_mine(bot_state)
        self.cached_result = result
        return result

    def construct(self):
        return GoToMineState()


class DefensiveState(BaseState):
    def __init__(self):
        super(DefensiveState, self).__init__()
        self.state_name = "DefensiveState"
        self.transitions = [
            Transition(lambda t: self.get_highest_projected_score(t) > self.my_projected_score(t),
                       lambda: GoToMineState())
        ]

    def execute_move(self, bot_state):
        return self.go_to_nearest_tavern(bot_state)

    def construct(self):
        return DefensiveState()
