import pandas as pd

class Model:
    def __init__(self, name, input_checker, buy_signal, sell_signal, rows_needed):
        '''
        input_checker takes a dataframe representing the available data, 
        and returns true if the data is the correct shape/size, false otherwise
        buy_signal takes a df and returns true if the model says to buy
        sell_signal also takes a df, but returns true if the model says to sell
        '''
        self.name = name
        self.check_input = input_checker
        self.buy_signal = buy_signal
        self.sell_signal = sell_signal
        self.rows_needed = rows_needed


class Mean_Reversion(Model):
    def __init__(self, name, n_for_long_ma, n_for_short_ma, n_for_RSI):
        '''
        implements a mean reversion strategy
        says buy if 1) price is higher than the 200_period_ma and 2) the 2_period_RSI is < 10
        says sell if price is lower than 10_period_ma
        '''
        self.name = name
        self.n_long_ma = n_for_long_ma
        self.n_short_ma = n_for_short_ma
        self.n_RSI = n_for_RSI
        self.expected_columns = [str(self.n_long_ma)+'_period_ma', str(self.n_short_ma)+'_period_ma', str(self.n_RSI)+'_period_RSI']
        self.rows_needed = 2

        def check_input(df):
            cols = df.columns
            for e in self.expected_columns:
                if not e in cols: return False
            return True

        def buy_signal(df):
            last_row = df.iloc[-1]
            condition1 = float(last_row['close_price']) > float(last_row[self.expected_columns[0]])
            # ^price > long ma
            condition2 = float(last_row[self.expected_columns[2]]) < 10
            # ^MSI < trigger
            return condition1 and condition2

        def sell_signal(df):
            last_row = df.iloc[-1]
            return float(last_row['close_price']) < float(last_row[self.expected_columns[1]])

        self.check_input = check_input
        self.buy_signal = buy_signal
        self.sell_signal = sell_signal

    def save(self):
        return
