
import vindinium as vin
from vindinium.bots import BaseBot
from vindinium.utils import AStar
import random

class BaseState(object):
    def __init__(self):
        self.transitions = []
        self.search = None
        self.state_name = "ERROR: BaseState"

    def get_state(self, bot_state):
        """

        :param bot_state:
        :type bot_state: BaseBot
        :return:
        """
        self.search = AStar(bot_state.game.map)
        for t in self.transitions:
            if t.is_valid(bot_state):
                print("state transition")
                v = t.state()
                v.search = self.search
                print("returning state {}".format(v.state_name))
                return v
        return self

    @staticmethod
    def hero_health_is_less_than(health_num):
        """

        :type health_num: Int
        :return:
        """
        def hero_health_is_less_than_internal(bot_state):
            """

            :type bot_state: BaseBot
            :param bot_state:
            :return:
            """

            print("health: {}, target health, {}".format(bot_state.hero.life, health_num))
            return bot_state.hero.life < health_num
        return hero_health_is_less_than_internal

    @staticmethod
    def hero_health_is_greater_than(health_num):
        """

        :type health_num: Int
        :return:
        """
        def hero_health_is_greater_than_internal(bot_state):
            """

            :type bot_state: BaseBot
            :param bot_state:
            :return:
            """
            return bot_state.hero.life > health_num
        return hero_health_is_greater_than_internal

    def _go_to(self, bot_state, x_, y_):
        x = bot_state.hero.x
        y = bot_state.hero.y

        # Compute path to the target
        path = self.search.find(x, y, x_, y_)

        # Send command to follow that path
        if path is None:
            return

        elif len(path) > 0:
            x_, y_ = path[0]

        return vin.utils.path_to_command(x, y, x_, y_)

    def go_to_nearest_tavern(self, bot_state):
        x = bot_state.hero.x
        y = bot_state.hero.y

        # Order taverns by distance
        taverns = vin.utils.order_by_distance(x, y, bot_state.game.taverns)
        for tavern in taverns:
            command = self._go_to(bot_state, tavern.x, tavern.y)

            if command:
                return command

        return self._random()

    def go_to_nearest_mine(self, bot_state):
        x = bot_state.hero.x
        y = bot_state.hero.y

        # Order mines by distance
        mines = vin.utils.order_by_distance(x, y, bot_state.game.mines)
        for mine in mines:

            # Grab nearest mine that is not owned by this hero
            if mine.owner != bot_state.hero.id:
                command = self._go_to(bot_state, mine.x, mine.y)

                if command:
                    return command

        return self._random()

    def _random(self):
        return random.choice(['Stay', 'North', 'West', 'East', 'South'])

    def execute_move(self, bot_state):
        pass
