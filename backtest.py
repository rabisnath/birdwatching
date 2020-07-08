from world import *

class Universe:
    '''
    represents a collection of worlds to be used for a backtest
    '''
    def __init__(self, name, watchlist, world=None, spans=['year'], indicators=[], rows_needed=2):
        self.name = name
        self.rows_needed = rows_needed
        if world==None:
            w = world_from_live(watchlist, spans=spans, indicators=indicators)
            self.base_world = w
            self.current_world = w
        else:
            self.base_world = world
            self.current_world = world
        # add indicators to base_world
        # n_worlds = how many times one can advance/update the world while meeting criteria
    
    #sanity check: u.base_world.datasets['fb']['year'].data <- a dataframe

    def get_next_world(self):
        '''
        return self.current_world and update it for the next time this is called
        update the current world using methods of the world class
        '''
        return

    def compare(self):
        '''
        get summary stats of current_world vs base_world
        '''
        return

class Backtest:
    '''
    class to bundle functions for carrying out and summarizing backtests
    '''
    def __init__(self, name, investor, universe):
        self.name = name
        self.investor = investor
        self.universe = universe
        self.universe.rows_needed = investor.get_rows_needed()

    def do_backtest(self, options):
        '''
        carry out backtest
            give investor current world from universe
            call investor methods, update investor world to simulate trades
            track stats
            repeat
            summarize stats
        '''
        return
        