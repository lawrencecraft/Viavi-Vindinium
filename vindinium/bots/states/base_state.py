from vindinium.models import Game


class BaseState(object):
    def __init__(self):
        self.transitions = []

    def get_state(self, game):
        for t in self.transitions:
            if t.is_valid(game):
                return t.state

        return self

    def execute_move(self, game):
        pass
