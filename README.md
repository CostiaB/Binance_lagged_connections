# Binance lagged connections


There are two parts in this repository. First is a script to download data from Binance using their API. You can download data for as many crypto coins as you need simultaneously. The data would be returned in one data frame with a following columns: [ 'open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'qav',   'num_trades', 'taker_base_vol', 'taker_quote_vol', 'ignore' and 'Ticker_Full_Name' ] the coin name would be in  the  'Ticker_Full_Name' column. You can choose a list of coin names, start and end dates, and a type of candle.
     
Usage example:    

    from binance_download import download_data
    data = download_data(symbols = ['BTCUSDT', 'ADXUSDT'],
    start_day = '2022-07-07',
    interval = '1h',
    api_key,
    api_secret, 
    end_day = '2022-08-08')


The second part is a script for the analysis of lagged correlations. There are several useful functions for that research in the lagged_correlation.py file. You can search for correlations in all data divided into several windows or use a rolling window for that search. Also, there are functions to find the most frequent or most prominent lags. File binance_lag_corr.ipynb has the example of their usage for two coins data.
