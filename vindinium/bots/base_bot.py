from vindinium.models import Game


class BaseBot():
    '''Base bot.

    Attributes:
        id (int): the bot's id.
        game (vindinium.models.Game): the game instance, updated by this object.
        hero (vindinium.models.Hero): the bot's hero instance, updated by this 
          object.
        state (dict): the unprocessed state from server.
    '''
    id = None
    state = None
    game = None
    hero = None

    def _start(self, state):
        '''Wrapper to start method.'''
        self.id = state['hero']['id']
        self.state = state
        self.game = Game(state)
        self.hero = self.game.heroes[self.id-1]
        self.start()

    def _move(self, state):
        '''Wrapper to move method.'''
        self.state = state
        self.game.update(state)
        return self.move()

    def _end(self):
        '''Wrapper to end method.'''
        self.end()

    def start(self):
        '''Called when the game starts.'''
        pass

    def move(self):
        '''Called when the game requests a move from this bot.'''
        pass

    def end(self):
        '''Called after the game finishes.'''
        pass