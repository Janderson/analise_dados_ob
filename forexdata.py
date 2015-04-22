# -*- coding: utf-8 -*-
import pandas as pd

class IndicatorData:
    dir_of_files = "E:/TickDataDownloader/tickdata/"
    def __init__(self, par, indicator_name):
        self.par = par
        self.indicator_name = indicator_name
    
    def g_data(self, timeframe):
        try:
            filename = self.dir_of_files + self.par + "_" + timeframe + ".csv"
            dt = pd.read_csv(filename, sep = ";")
            return 
        except IOError as e:
            print "Data Not Found"
            return None
    

class FxData:
    dir_of_files = "d:/TickDataDownloader/tickdata/____COMPLETE_DATA_____/"
    def __init__(self, par):
        self.par = par
    
    def g_data(self, timeframe):
        filename = self.dir_of_files +self.par + "_" + timeframe + ".csv"
        return pd.read_csv(filename, parse_dates=[0], header=None, 
                           names=['date', 'open', 'high', 'low', 'close', 'volume', 'tickvol'])
        

if __name__=="__main__":
    print "For debugging only"
    fxDt = FxData("GBPJPY")
    dt = fxDt.g_data("H1")
    print dt.head()
        