import pandas as pd
from binance.client import Client


def download_data(symbols:list,
                  start_day:str,
                  interval:str,
                  api_key:str,
                  api_secret:str,
                  end_day=None
                  ):
    '''
    
    Parameters
    ----------
    symbols : list[str]
        List of symbol names
    start_day : str
        first day to download string in UTC format (YYYY-MM-DD)
    interval : str
        type of a candles interval variants: '1m', '3m', '5m', '15m', '30m',
        '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'
    api_key : str
        binance api key
    api_secret : str
        binance api secret key
    end_day :str 
        optional - end date string in UTC format (if not submitted it will
                                                  fetch everything up to now)
    
    
    Returns
    -------
    data : pd.dataframe
        Dataframe with 'open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'qav',
        'num_trades', 'taker_base_vol', 'taker_quote_vol', 'ignore' and 'Ticker_Full_Name' columns
        for asked symbol and start date 
    '''
    client = Client(api_key, api_secret)
    columns = ['open_time', 'open', 'high', 'low', 'close', 'volume','close_time', 'qav',
                    'num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
    data = pd.DataFrame(columns = columns)
 
    for s in symbols:
        print(f'Downloading {s} data')
        if end_day:
            klines = client.get_historical_klines(s, interval, start_day,
                                                  end_str=end_day)
        else:
            klines = client.get_historical_klines(s, interval, start_day)
        tmp = pd.DataFrame(klines, columns=columns)
        tmp.loc[:, 'Ticker_Full_Name'] = s
        data = pd.concat([data, tmp])
        data = data.reset_index(drop = True)
    return data