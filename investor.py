import robin_stocks as r

class Investor_settings:
    '''
    a standardized group of settings characterizing the behavior of 
    the investor class
    # should add settings for the routine method too
    '''
    def __init__(self, **kwargs):
        self.max_risk = kwargs.pop('max_risk', 0.10) # max % of cash to spend at once
        self.desired_risk = kwargs.pop('desired_risk', 0.05) # % of cash to spend at once
        self.max_trades = kwargs.pop('max_trades', 1) # max # of trades per call of i.routine()
        self.order_type = kwargs.pop('order_type', 'market') # use market or limit orders
        self.use_stop = kwargs.pop('use_stop', False) # use a stop?
        self.time_in_force = kwargs.pop('time_in_force', 'gfd') # how long orders are good for
        # ‘gtc’ = good until cancelled. ‘gfd’ = good for the day. ‘ioc’ = immediate or cancel. ‘opg’ execute at opening
        self.verbosity = kwargs.pop('verbosity', 1)
        self.name = kwargs.pop('name', 'Default Investor')

class Investor:
    '''
    the investor class takes a model, a world, some settings, and generates ideas
    for concrete trades to execute
    '''
    def __init__(self, models, world, settings=Investor_settings(), live=False):
        self.models = models
        self.world = world
        self.settings = settings
        self.live = live

    def get_rows_needed(self):
        '''
        look at self.models, return max of m.rows_needed
        '''
        return max([m.rows_needed for m in self.models])

    def get_buy_quantity(self, p):
        cash = self.world.cash
        max_ = self.settings.max_risk * cash
        if p > max_:
            return 0
        else:
            return int(self.settings.desired_risk * cash)

    def get_sell_quantity(self, symbol):
        return int(self.world.holdings[symbol]['quantity'])

    def get_trade(self, symbol, p, side):
        q = get_buy_quantity(p) if side=='buy' else get_sell_quantity(symbol)
        if q == 0: return None
        kwargs = {
            'symbol': symbol,
            'quantity': q,
            'orderType': self.settings.order_type,
            'side': side,
            'timeInForce': self.settings.time_in_force
        }

        if self.settings.order_type == 'limit':
            kwargs['limitPrice'] = p

        if self.settings.use_stop:
            kwargs['trigger'] = 'stop'
            kwargs['stopPrice'] = p
        else:
            kwargs['trigger'] = 'immediate'

        t = {
            'symbol': symbol,
            'price': p,
            'side': side,
            'quantity': q, 
            # ^most of these are already in kwargs, but its nice to have them here
            # for when the backtesting script sees the trades
            'kwargs': kwargs
        }
        return t

    def get_suggested_trades(self):
        '''
        for model in self.models:
            ask model, should I trade?
            ask settings, how to trade?
            output list of trade objs
        '''
        trades = []
        for symbol in self.world.watchlist:
            for m in self.models:
                span = m.span
                data = self.world.datasets[symbol][span].data
                if len(data) > self.get_rows_needed(): continue
                if not m.check_input(data): continue
                buy = m.buy_signal(data)
                sell = m.sell_signal(data)
                print("thinking about " + symbol + ' with model ' + m.name)
                print("buy: " + str(buy), "sell: " + str(sell))
                if buy + sell != 1: continue
                if self.live:
                    p = float(r.stocks.get_latest_price(symbol)[0])
                else:
                    p = float(data.loc[-1, 'close_price'])
                if buy:
                    t = get_trade(symbol, p, 'buy')
                    if t != None:
                        trades.append(t)
                if sell and symbol in self.world.holdings.keys():
                    t = get_trade(symbol, p, 'sell')
                    if t != None:
                        trades.append(t)

        return trades

    def execute_trade(self, t):
        '''
        if live, actually make the trade, else print details to console
        '''
        if self.settings.verbosity == 1:
            print(t['side']+'ing '+t['quantity']+' shares of '+t['symbol']+' at '+str(t['price']))
        if self.live:
            r.order(**t['kwargs'])
        else:
            if self.settings.verbosity == 1:
                print("would call r.order() with these params: ", t['kwargs'])
        return

    def routine(self):
        '''
        do everything the investor is expected to do on a given day
        essentially, call each of the class methods
        '''
        trades = self.get_suggested_trades()
        print("running routine, found {} trades".format(len(trades)))
        for t in trades:
            self.execute_trade(t)
        return