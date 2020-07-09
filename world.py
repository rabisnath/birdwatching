import pandas as pd
import robin_stocks as r
from datetime import datetime 
import copy

'''
df.head               begins_at  open_price close_price  high_price   low_price    volume session  interpolated symbol  200_period_ma  10_period_ma  2_period_RSI
0  2019-07-03T00:00:00Z  203.280000  204.410000  204.440000  202.690100  11362045     reg         False   AAPL     204.410000    204.410000     50.000000
1  2019-07-05T00:00:00Z  203.350000  204.230000  205.080000  202.900000  17265518     reg         False   AAPL     204.320000    204.320000     50.124688
2  2019-07-08T00:00:00Z  200.810000  200.020000  201.400000  198.410000  25338628     reg         False   AAPL     202.886667    202.886667     50.124688
3  2019-07-09T00:00:00Z  199.200000  201.240000  201.510000  198.810000  20578015     reg         False   AAPL     202.475000    202.475000     59.349593
4  2019-07-10T00:00:00Z  201.850000  203.230000  203.730000  201.560000  17897138     reg         False   AAPL     202.626000    202.626000     63.099631 

columns Index(['begins_at', 'open_price', 'close_price', 'high_price', 'low_price',
       'volume', 'session', 'interpolated', 'symbol', '200_period_ma',
       '10_period_ma', '2_period_RSI'],
      dtype='object')
'''

'''
>>> r.account.build_holdings()
{'FIT': {'price': '6.220000', 'quantity': '1.00000000', 'average_buy_price': '0.0000', 
'equity': '6.22', 'percent_change': '0.00', 'equity_change': '6.220000', 'type': 'stock', 
'name': 'Fitbit', 'id': 'fdf46795-2a81-4506-880f-514c8010c163', 'pe_ratio': None, 'percentage': '100.00'}}
'''

class Dataset:
    '''
    this class and its subclasses provide a layer of abstraction between a given dataset
    and the other tools in this package so changes in convention from one broker
    to another can all be handled at once and the rest of the package can refer to standard
    column names and conventions
    '''
    def __init__(self, name, data, metadata, column_guide, recent_last):
        self.name = name
        self.data = data
        self.metadata = metadata
        self.column_guide = column_guide
        self.recent_last = recent_last

    def add_indicators(self, indicators):
        # add indicators/metrics to dataframes
        for i in indicators:
            i.apply(self.data)
        return

    def get_subset(self, i, n_rows):
        '''
        returns a copy of self where self.data = self.data[i: i+nrows]
        '''
        new_ds = copy.deepcopy(self)
        new_ds.data = new_ds.data[i: i+n_rows]
        return new_ds

        

class Robinhood_Data(Dataset):
    def __init__(self, data, symbol, span, note=''):
        self.name = 'rh_data_'+symbol+'_'+span+'_'+str(data.loc[0, 'begins_at'])
        self.data = data
        self.metadata = {
            'symbol': symbol,
            'span': span,
            'note': note,
        }
        # in the future, dataset classes for other brokers would have col guides w
        # same keys, different values, functions pkg wide will refer to these keys
        self.column_guide = {
            'begins_at': 'begins_at',
            'open_price': 'open_price',
            'close_price': 'close_price',
            'high_price': 'high_price',
            'low_price': 'low_price',
            'volume': 'volume',
            'session': 'session',
            'interpolated': 'interpolated',
            'symbol': 'symbol',
        }
        self.recent_last = True

class World:
    '''
    The world class is the 'environment' within which the investor/model classes operate
    this layer of abstraction allows changing from backtesting to livetrading and back without
    changing the code that makes decisions
    '''
    def __init__(self, name, cash, holdings, watchlist, datasets, indicators=[]):
        self.name = name
        self.cash = cash
        self.holdings = holdings
        self.watchlist = watchlist
        self.datasets = datasets
        #datasets is a multi-level dict with keys for symbol, span, Dataset values
        #datasets['TSLA']['year'].data == r.get_historicals('TSLA', span='year')
        self.indicators = indicators
        self.add_indicators()

    def get_sub_datasets(self, i, n_rows):
        # for updating the world during backtesting

        #for symbol, span_dict in self.datasets.items():
        #    for span, dataset in span_dict.items():
        #        dataset = dataset.get_subset(i, n_rows)

        #new_wrld = copy.deepcopy(self)
        #new_wrld.datasets = {sym: {span: dataset.get_subset(i, n_rows) for span, dataset in span_dict.items()} for sym, span_dict in self.datasets.items()}

        #return new_wrld

        return {sym: {span: dataset.get_subset(i, n_rows) for span, dataset in span_dict.items()} for sym, span_dict in self.datasets.items()}

    def update_from_live(self, spans=['year']):
        # for updating the world during livetrading
        self.cash = float(r.account.build_user_profile()['cash'])
        self.holdings = r.account.build_holdings()
        self.datasets = {symbol:{span: get_RH_dset(symbol, span) for span in spans} for symbol in self.watchlist}
        self.add_indicators()
        return

    def add_indicators(self):
        # call add_indicators method for each indicator on each dataset
        for symbol, span_dict in self.datasets.items():
            for span, dataset in span_dict.items():
                dataset.add_indicators(self.indicators)
        return

    def update_holdings(self, symbol, price, quantity, mode='buy'):
        # update holdings during backtesting
        if symbol in self.holdings.keys():
            if mode == 'buy':
                self.holdings[symbol]['quantity'] += quantity
            elif mode == 'sell':
                self.holdings[symbol]['quantity'] -= quantity
            self.holdings[symbol]['price'] = price
        else:
            if mode != 'buy':
                raise KeyError("can't sell stock not in portfolio")
            self.holdings[symbol] = {
                'price': price,
                'quantity': quantity,
            }
        return

def get_RH_dset(symbol, span, note=''):
    # span \in ['day', 'week', 'month', '3month', 'year', '5year']
    return Robinhood_Data(pd.DataFrame(r.get_historicals(symbol, span=span)), symbol, span, note=note)    

def world_from_live(watchlist, **kwargs): #, spans=['year'], indicators=[], get_dset=get_RH_dset):
    '''
    creates a world object representing the current world
    '''
    spans = kwargs.pop('spans', ['year'])
    get_dset = kwargs.pop('get_dset', get_RH_dset)
    w = World(name='live_world_'+datetime.now().strftime("%D"), 
            cash= kwargs.pop('cash', float(r.account.build_user_profile()['cash'])),
            holdings=r.account.build_holdings(),
            watchlist=watchlist,
            datasets={symbol:{span: get_dset(symbol, span) for span in spans} for symbol in watchlist},
            indicators=kwargs.pop('indicators', [])
    )

    return w


if __name__ == '__main__':
    
    user = 'alex.bisnath@gmail.com'
    pword = ''

    basket = ['FB','AAPL','TSLA','NFLX']

    r.login(user, pword)

    from indicators import Moving_Average, RSI

    w = world_from_live(basket, indicators=[Moving_Average(n=200), Moving_Average(n=10), RSI(2)])

    print(w.datasets['TSLA']['year'].data['200_period_ma'])



