class Transition(object):
    def __init__(self, condition, state):
        self.condition = condition
        self.state = state

    def is_valid(self, bot_state):
        return self.condition(bot_state)
