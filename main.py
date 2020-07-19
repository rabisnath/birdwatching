import robin_stocks as r
import pandas as pd

user = 'alex.bisnath@gmail.com'
pword = ''

def print_data(symbols, span):
    data = r.get_historicals(symbols, span=span)
    print("\n data for {}, {}:\n".format(str(symbols), span))
    print(data)
    return 

if __name__ == "__main__":
    
    r.login()

    # setting watchlist
    #basket = ['FB','AAPL','TSLA','NFLX']
    basket = list(pd.read_csv('snp500.csv')['Symbol'].values)[:10]
    
    #holdings = r.build_holdings()
    #profile = r.load_account_profile()

    #print("\nHoldings:\n")
    #for k,v in holdings.items():
    #    print(k, v)

    #print("\nProfile:\n")
    #for k,v in profile.items():
    #    print(k, v)

    #print_data(basket[0], 'day') #5min intervals
    #print_data(basket[0], 'week') #10min
    #print_data(basket[0], 'month') #1hr
    #print_data(basket[0], '3month') #1hr
    #print_data(basket[0], 'year') #daily
    #print_data(basket[0], '5year') #weekly

    #print(r.get_quotes(basket))
    #print(r.account.build_holdings())
    #print(r.account.build_user_profile())

    # --- workflow 1 ---
    '''
    # getting data
    data = r.get_historicals(basket[1], span='year')
    df = pd.DataFrame(data)
    #print("df.head", df.head(), "\n")
    #print("columns", df.columns)
    
    # adding indicators
    from indicators import add_moving_average, add_RSI
    add_moving_average(df, n=200)
    add_moving_average(df, n=10)
    add_RSI(df, n=2)

    # creating a model
    from models import Mean_Reversion
    strat = Mean_Reversion('MR', 200, 10, 2)
    print("\nchecking data:")
    print(strat.check_input(df))
    print("\nbuy signal:")
    print(strat.buy_signal(df))
    print("\nsell signal:")
    print(strat.sell_signal(df),'\n')
    '''

    # --- workflow 2 ---
    '''
    # build world
    from indicators import Moving_Average, RSI
    from world import world_from_live
    w = world_from_live(basket, cash=10000, indicators=[Moving_Average(n=200), Moving_Average(n=10), RSI(2)])
    # get model
    from models import Mean_Reversion
    mr = Mean_Reversion('Mean Reversion', 200, 10, 2)
    # build investor
    from investor import Investor
    investor = Investor(models=[mr], world=w, live=False)
    # livetrade with investor
    investor.routine()
    '''

    # --- workflow 3 ---
    
    # build base world
    from indicators import Moving_Average, RSI
    from world import world_from_live
    w = world_from_live(basket, cash=10000, indicators=[Moving_Average(n=200), Moving_Average(n=10), RSI(2)])
    # get model
    from models import Mean_Reversion
    mr = Mean_Reversion('Mean Reversion', 200, 10, 2)
    # build investor
    from investor import Investor
    i = Investor(models=[mr], world=w, live=False)
    # set up backtest
    from backtest import Backtest
    b = Backtest(name='mean_reversion_backtest_000', investor=i, base_world=w)
    # show/export results
    b.do_backtest()
    b.export_history(path='backtests/')

    # --- workflow 4 ---

    # neural ODE model class / some other trainable model
    # that will allow us to good make use of the backtesting tools

    # --- workflow 5 --- 

    # exporting, importing model
    # test many models against each other
    # export best ones




    r.logout()