from world import *
import copy
import pandas as pd

class Backtest:
    '''
    tools for papertrading a model over some provided dataset
    '''
    def __init__(self, name, investor, base_world, verbosity=1):
        self.name = name
        self.investor = investor
        self.investor.live = False
        self.verbosity = verbosity
        self.investor.settings.verbosity = verbosity
        self.base_world = copy.deepcopy(base_world)
        self.current_world = copy.deepcopy(base_world)
        self.rows_needed = self.investor.get_rows_needed()
        self.history = pd.DataFrame(columns=['time', 'cash_before_trade', 'symbol', 'quantity', 'price', 'side'])
        self.time = 0
        self.max_time = max([len(ds.data) for span_dict in self.base_world.datasets.values() for ds in span_dict.values()]) - self.rows_needed
        

    #sanity check: b.base_world.datasets['fb']['year'].data <- a dataframe

    def set_max_time(self, t):
        self.max_time = t

    def update(self):
        '''
        updates self.current_world, self.history based on a series of trades
        '''
        if self.time > self.max_time: return False
        # update self.current_world
        self.current_world.datasets = self.base_world.get_sub_datasets(self.time, self.rows_needed)
        self.investor.world = self.current_world
        trades = self.investor.get_suggested_trades()
        # update cash, holdings, history
        for t in trades:
            self.investor.execute_trade(t) # just to get a print out of the trade
            
            self.history = self.history.append({
                'time': self.time,
                'cash_before_trade': self.current_world.cash, 
                'symbol': t['symbol'], 
                'quantity': t['quantity'], 
                'price': t['price'], 
                'side': t['side'],
            }, ignore_index=True)

            #self.history.append(
            #    pd.DataFrame([[self.time, self.current_world.cash, t['symbol'], t['quantity'], t['price'], t['side']]], 
            #        columns=['time', 'cash_before_trade', 'symbol', 'quantity', 'price', 'side']),
            #    ignore_index=True)
            
            q = int(t['quantity'])
            p = float(t['price'])

            if t['side'] == 'buy':
                self.current_world.cash -= q * p
                self.current_world.update_holdings(t['symbol'], p, q, mode='buy')
            if t['side'] == 'sell':
                self.current_world.cash += q * p
                self.current_world.update_holdings(t['symbol'], p, q, mode='sell')

        self.time += 1
        return True
    
    def export_history(self, path='', mode='csv'):
        '''
        save self.history to .csv or some other format
        '''
        if mode == 'csv':
            self.history.to_csv(path+self.name+'.csv')
        return

    def make_summary(self):
        '''
        how many trades?
        how many profitable trades?
        portfolio value at end of backtest vs beginning?
        % return?
        '''
        # ['time', 'cash_before_trade', 'symbol', 'quantity', 'price', 'side'])
        #df = self.history

        summary = {
            'starting cash': self.base_world.cash,
            'ending cash': self.current_world.cash,
            'percent gain': 100 * (self.current_world.cash - self.base_world.cash) / self.base_world.cash,
        }

        return summary

    def plot_results(self):
        '''
        make line chart of portfolio value over the backtesting period
        '''
        return

    def do_backtest(self):
        '''
        iteratively call self.update and report results
        '''
        self.time = 0
        while self.update(): self.time += 1
        if self.verbosity > 0:
            for k, v in self.make_summary().items():
                print("{}: {}".format(k, v))
            print("Holdings at end of backtest: ", self.current_world.holdings)

        return
        