
import vindinium as vin
from vindinium.bots import BaseBot
from vindinium.utils import AStar
import random

class BaseState(object):
    def __init__(self):
        self.transitions = []
        self.search = None
        self.state_name = "ERROR: BaseState"
        self.cost_threshold = 1000

    def get_state(self, bot_state):
        """

        :param bot_state:
        :type bot_state: BaseBot
        :return:
        """
        self.search = AStar(bot_state.game.map, bot_state)
        for t in self.transitions:
            if t.is_valid(bot_state):
                print("state transition")
                v = t.state()
                v.search = self.search
                print("returning state {}".format(v.state_name))
                return v
        new_state = self.construct()
        new_state.search = AStar(bot_state.game.map, bot_state)
        return new_state

    def construct(self):
        pass

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

    @staticmethod
    def gold_is_greater_than(num_gold):
        def gold_is_greater_than_internal(bot_state):
            """

            :type bot_state: BaseBot
            :param bot_state:
            :return:
            """
            return bot_state.hero.gold > num_gold
        return gold_is_greater_than_internal

    @staticmethod
    def nearest_tavern_is():
        def nearest_tavern_internal(bot_state):
            """

            :type bot_state: BaseBot
            :param bot_state:
            :return:
            """
            tavern_distances = [vin.utils.distance_manhattan(bot_state.hero.x, bot_state.hero.y, t.x, t.y)
                                for t in bot_state.game.taverns]
            return min(tavern_distances)
        return nearest_tavern_internal

    def _go_to(self, bot_state, x_, y_):
        x = bot_state.hero.x
        y = bot_state.hero.y
        hero_tiles = set()

        for hero in bot_state.game.heroes:
            if hero == bot_state.hero:
                continue
            hero_tiles.add((hero.x, hero.y))
            hero_tiles.add((hero.x+1, hero.y))
            hero_tiles.add((hero.x-1, hero.y))
            hero_tiles.add((hero.x, hero.y-1))
            hero_tiles.add((hero.x, hero.y+1))
            hero_tiles.add((hero.x-1, hero.y-1))
            hero_tiles.add((hero.x+1, hero.y-1))
            hero_tiles.add((hero.x-1, hero.y+1))
            hero_tiles.add((hero.x+1, hero.y+1))

        # Compute path to the target
        path, cost = self.search.find(x, y, x_, y_, hero_tiles)
        # if cost > self.cost_threshold:
        #     self.cost_threshold *= 2
        #     print("Standing still")
        #     return 'Stay', cost
        self.cost_threshold = 1000
        # Send command to follow that path
        if path is None:
            return

        elif len(path) > 0:
            x_, y_ = path[0]

        return vin.utils.path_to_command(x, y, x_, y_), cost

    def go_to_nearest_tavern(self, bot_state):
        x = bot_state.hero.x
        y = bot_state.hero.y

        # Order taverns by distance
        taverns = vin.utils.order_by_distance(x, y, bot_state.game.taverns)
        tavern_list = taverns[:5]
        min_cost = 999999999
        final_command = None
        for tavern in tavern_list:
            command, cost = self._go_to(bot_state, tavern.x, tavern.y)
            if cost < min_cost:
                min_cost = cost
                final_command = command

        if final_command:
            return final_command

        return self._random()

    def go_to_nearest_mine(self, bot_state):

        x = bot_state.hero.x
        y = bot_state.hero.y

        # Order mines by distance
        mines = [m for m in vin.utils.order_by_distance(x, y, bot_state.game.mines) if m.owner != bot_state.hero.id]
        mines_to_search = mines[:5]
        min_cost = 9999999999
        final_command = None
        for mine in mines_to_search:
            command, cost = self._go_to(bot_state, mine.x, mine.y)

            if cost < min_cost and command:
                final_command = command
                min_cost = cost

        if final_command:
            return final_command, min_cost
        print("this should not happen")
        return self._random(), 9000

    @staticmethod
    def nearest_neighbor(bot_state):
        """

        :type bot_state: BaseBot
        """
        distances = [vin.utils.distance_manhattan(bot_state.hero.x, bot_state.hero.y, e.x, e.y) for e in bot_state.game.heroes if e.id != bot_state.hero.id]
        return min(distances)

    @staticmethod
    def get_highest_projected_score(bot_state):
        """

        :type bot_state: BaseBot
        """
        return max([BaseState.project_score(hero, bot_state.game) for hero in bot_state.game.heroes
                    if hero.id != bot_state.hero.id])

    @staticmethod
    def my_projected_score(bot_state):
        return BaseState.project_score(bot_state.hero, bot_state.game)

    @staticmethod
    def project_score(hero, game):
        """

        :type game: vin.models.Game
        :type hero: vin.models.Hero
        """
        return (int(game.max_turns) - int(game.turn)) * int(hero.mine_count) + int(hero.gold)

    def game_is_almost_over(self, bot_state):
        percentage = self.game_percentage(bot_state.game)
        print "Game percentage: {}".format(percentage)
        return percentage > 0.75

    def game_percentage(self, game):
        print "Turn {}".format(game.turn)
        return float(game.turn) / int(game.max_turns)

    def _random(self):
        return random.choice(['Stay', 'North', 'West', 'East', 'South'])

    def execute_move(self, bot_state):
        pass
