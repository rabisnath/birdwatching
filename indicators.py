import pandas as pd

def add_moving_average(df, n, use_price='close_price'):
    '''
    adds a new column to df called 'n_period_ma' with the moving 
    average of the column $use_price over n data points
    '''
    new_col = []
    col_name = str(n)+'_period_ma'
    i = 0
    while i < len(df):
        if i == 0:
            new_col.append(float(df[use_price][0]))
        elif i < n:
            total = 0
            for j in range(i+1):
                total += float(df.iloc[j][use_price])
            new_col.append(total/(i+1))
        else:
            total = 0
            for j in range(i-n, i):
                total += float(df.iloc[j][use_price])
            new_col.append(total/n)
        i += 1
    df[col_name] = new_col

    return

def add_RSI(df, n):
    '''
    adds a new column to df called 'n_period_RSI' with the RSI 
    calculated over the last n data points
    '''
    new_col = []
    col_name = str(n)+'_period_RSI'
    i = 0
    while i < len(df):
        if i == 0:
            new_col.append(50)
        else:
            gains = []
            losses = []
            for j in range(max([0, i-n]), i+1):
                open_price = float(df.iloc[j]['open_price'])
                close_price = float(df.iloc[j]['close_price'])
                diff = close_price - open_price
                if diff > 0:
                    gains.append(diff)
                else:
                    losses.append(diff)
            avg_gain = sum(gains)/max([len(gains), 1]) # using max to avoid a div by zero error
            avg_loss = sum(losses)/max([len(losses), 1])
            RS = avg_gain / max([avg_loss, 1])
            new_col.append(100 - (100/(1+RS)))
        i += 1
    df[col_name] = new_col

    return

if __name__ == '__main__':
    pass
    #df = pd.DataFrame(facebook_5min)
    #add_moving_average(df, 20)
    #add_RSI(df, 2)
    #print(df.head())