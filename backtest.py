from world import *
import copy
import pandas as pd

class Backtest:
    '''
    tools for papertrading a model over some provided dataset
    '''
    def __init__(self, name, investor, base_world):
        self.name = name
        self.investor = investor
        self.base_world = copy.deepcopy(base_world)
        self.current_world = copy.deepcopy(base_world)
        self.rows_needed = self.investor.get_rows_needed()
        self.history = pd.DataFrame(columns=['time', 'cash_before_trade', 'symbol', 'quantity', 'price', 'side'])
        self.time = 0
        self.max_time = max([len(ds.data) for span_dict in self.base_world.datasets.values() for ds in span_dict.values()]) - self.rows_needed

    #sanity check: b.base_world.datasets['fb']['year'].data <- a dataframe

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
            self.history.append({
                'time': self.time,
                'cash_before_trade': self.current_world.cash, 
                'symbol': t['symbol'], 
                'quantity': t['quantity'], 
                'price': t['price'], 
                'side': t['side'],
            }, ignore_index=True)
            
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
    
    def export_history(self):
        '''
        save self.history to .pkl or some other format
        '''
        return

    def summary_stats_from_history(self):
        '''
        how many trades?
        how many profitable trades?
        portfolio value at end of backtest vs beginning?
        % return?
        '''
        return

    def plot_results(self):
        '''
        make line chart of portfolio value over the backtesting period
        '''
        return

    def do_backtest(self, **kwargs):
        '''
        iteratively call self.update and report results
        '''

        return
        