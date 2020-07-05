import robin_stocks as r
import pandas as pd

user = 'alex.bisnath@gmail.com'
pword = ''

basket = ['fb','aapl','tsla','nflx']

def print_data(symbols, span):
    data = r.get_historicals(symbols, span=span)
    print("\n data for {}, {}:\n".format(str(symbols), span))
    print(data)
    return 

if __name__ == "__main__":
    
    r.login(user, pword)
    
    #holdings = r.build_holdings()
    #profile = r.load_account_profile()

    #print("\nHoldings:\n")
    #for k,v in holdings.items():
    #    print(k, v)

    #print("\nProfile:\n")
    #for k,v in profile.items():
    #    print(k, v)

    #print_data(basket[0], 'day') #5min
    #print_data(basket[0], 'week') #10min
    #print_data(basket[0], 'month') #1hr
    #print_data(basket[0], '3month') #1hr
    #print_data(basket[0], 'year') #daily
    #print_data(basket[0], '5year') #weekly

    #print(r.get_quotes(basket))
    #print(r.account.build_holdings())
    #print(r.account.build_user_profile())

    # --- workflow 1 ---

    # getting data
    data = r.get_historicals(basket[1], span='year')
    df = pd.DataFrame(data)
    #print("df.head", df.head(), "\n")
    #print("columns", df.columns)
    
    # adding indicators
    from indicators import add_moving_average, add_RSI
    add_moving_average(df, 200)
    add_moving_average(df, 10)
    add_RSI(df, 2)

    # creating a model
    from models import Mean_Reversion
    strat = Mean_Reversion('MR', 200, 10, 2)
    print("\nchecking data:")
    print(strat.check_input(df))
    print("\nbuy signal:")
    print(strat.buy_signal(df))
    print("\nsell signal:")
    print(strat.sell_signal(df),'\n')

    # --- workflow 2 ---

    # set watchlist
    # build world
    # get model
    # build investor
    # livetrade with investor

    # --- workflow 3 ---

    # set watchlist
    # build universe
    # get model
    # build investor
    # backtest with investor + universe

    # --- workflow 4 ---

    # neural network model class



    r.logout()