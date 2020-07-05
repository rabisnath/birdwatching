

class Investor_settings:
    '''
    a standardized group of settings characterizing the behavior of 
    the investor class
    # should add settings for the routine method too
    '''
    def __init__(self, max_risk, max_trades):
        self.risk = max_risk
        self.trades = max_trades

default_investor_settings = Investor_settings(0.05, 2)

class Trade:
    '''
    an object with details about a trade to execute
    investor class -> trade object -> a real trade OR results for backtesting fn's
    '''
    def __init__(self, symbol, quantity, order_type='market'):
        # to do: add params to match r.orders.order()
        self.symbol = symbol
        self.quantity = quantity
        self.order_type = order_type


class Investor:
    '''
    the investor class takes a model, a world, some settings, and generates ideas
    for concrete trades to execute
    '''
    def __init__(self, name, models, world, settings=default_investor_settings, live=False):
        self.name = name
        self.models = models
        self.world = world
        self.settings = settings
        self.live = live

    def get_rows_needed(self):
        '''
        look at self.models, return max of m.rows_needed
        '''
        return

    def get_suggested_trades(self):
        '''
        for model in self.models:
            ask model, should I trade?
            ask settings, how to trade?
            output list of trade objs
        '''
        return

    def refine_trades(self, trades):
        '''
        takes a list of suggested trades,
        uses info about current cash, holdings, to rate the viability
        of each trade 
        '''
        return

    def execute_trade(self, trade):
        '''
        if live, actually make the trade
        '''
        return

    def routine(self):
        '''
        do everything the investor is expected to do on a given day
        essentially, call each of the class methods
        '''
        return