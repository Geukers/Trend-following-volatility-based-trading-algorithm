import numpy as np

#set number of weeks in which you want to see return
return_period_days = 60

#I want at least this much average return
min_avg_return  = 5

#I want at most this much volatility in return
max_dev_return = 10

STOCK = "NVDA"

class VolatilityBasedGrowthAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2017, 1, 1) 
        self.SetEndDate(2020, 1, 1) 
        self.SetCash(100000)   
        
        self.stock = self.AddEquity(STOCK, Resolution.Daily)
        
        self.SetBenchmark("SPY")  
        self.SetWarmUp(return_period_days + 1)
        self.closeWindow = RollingWindow[float](return_period_days)
        self.lastMonthsWindow = RollingWindow[float](return_period_days)
        
    def OnData(self, data):
        self.closeWindow.Add(data[STOCK].Close)
        
        # Don't place trades until our indicators are warmed up:
        if self.IsWarmingUp:
            return
            
        closeWindowArray = []
        
        for i in self.closeWindow:
            closeWindowArray.append(i)
        
        last_months_return = (1 - np.average(closeWindowArray[30:59]) / np.average(closeWindowArray[::29])) * 100
        last_months_volatility = np.std(closeWindowArray)
        
        # self.Debug("Return : " + str(last_months_return))
        # self.Debug("Std. Dev : " + str(last_months_volatility))
        
        #1. If SPY has more upward momentum than BND, then we liquidate our holdings in BND and allocate 100% of our equity to SPY
        if last_months_return > min_avg_return and last_months_volatility < max_dev_return:
            self.SetHoldings(STOCK, 1)
            self.Debug("Bought!")

        #2. Otherwise we liquidate our holdings in SPY and allocate 100% to BND
        else:
            self.Liquidate(STOCK)
            self.Debug("Sold!")
