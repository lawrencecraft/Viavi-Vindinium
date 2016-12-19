from vindinium.bots.states import BaseState


class GoToMineState(BaseState):
    def execute_move(self, game):
        print("doing a move")

    def get_state(self, game):
        pass
