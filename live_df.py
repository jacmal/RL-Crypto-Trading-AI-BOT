import pandas as pd
import numpy as np

import os
import time
import threading

from requests import get
from datetime import datetime

class LiveDF:
    def __init__(self):
        self.df_file_name = 'test_live_data.csv'
        self.main_dir_path = ''
        self.df = None
        self.exitf = False
    
    def set_data_path_name(self, path, name):
        self.df_file_name = name
        self.main_dir_path = path
        os.chdir(self.main_dir_path)
    
    def start_data(self):
        threading.Thread(target=self._loop_time_window).start()
        print("Start data")
                
    def stop_data(self):
        self.exitf = True
        print("Stop data")
    
    def _init_test_df(self):
        self.df = pd.DataFrame(self._time_window(), index=[0])
        print(self.df)
    
    def _btc_price_now(self):
        link = 'https://api.coindesk.com/v1/bpi/currentprice.json'
         
        response = get(link)
        data = response.json()
        price_str = data['bpi']['USD']['rate']
         
        # cleaning text prices and convert it to "float" type
        price_clean = ''
        for x in price_str:
            if x in ['0','1','2','3','4','5','6','7','8','9','.']:
                price_clean += x
        current_price = float(price_clean)
         
        return current_price
     
    def _time_window(self, window_seconds=10, data_point_window=1):
        '''
        The function tracks the price of bitcoin over a set time period.
        Return dict: {
                      'Date': actual date
                      'price_open': time interval opening price
                      'price_close': time inrterval closing price
                      'price_min': timie interval minimum price
                      'price_max': timee interval maximum price
                      'price_avg': timee interval average price
                      }

        Args:
        (int) window_seconds    - size of the time window in seconds
        (int) data_point_window - price sampling from page in seconds

        Rerturns:
        (dict) all_prices - dictionary with prices data 
        '''
         
        # check bitcoin actual price and append it into "prices" list
        #price_link = 'https://api.coindesk.com/v1/bpi/currentprice.json'
                      
        prices = []
         

        for i in range(int(window_seconds / data_point_window)):
            price = self._btc_price_now()
            prices.append(price)
            time.sleep(data_point_window)
            if self.exitf == True:
                print('zatrzymales')
                break
                
        # create dictionary with output data
        all_prices = {}
         
        all_prices['Date'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        all_prices['price_open'] = prices[0]
        all_prices['price_min'] = min(prices)
        all_prices['price_max'] = max(prices)
        #all_prices['price_avg'] = np.mean(prices)
        all_prices['price_close'] = prices[-1]
         
        #print(all_prices)
        return all_prices
    
    def _loop_time_window(self):
        #os.chdir('H:\Mój dysk')
        #file_name = 'test_live_data.csv'
        while not self.exitf:
            live_data = self._time_window()
            if self.exitf == False:
                live_df = pd.DataFrame(data=live_data, index=[0])
                self.df = pd.concat([self.df, live_df], ignore_index=True)
                self.df.to_csv(self.df_file_name)
                
                #TSESTING
                try:
                    from IPython import get_ipython
                    get_ipython().magic('clear')
                    os.system('cls')
                except:
                    pass
                print(self.df)
        print('exit without saving!!!')

    def data_time_window(self, window_size):
        if len(self.df) > 9:
            return self.df.iloc[-window_size:, :]
        else:
            print(len(self.df))
            return self.df