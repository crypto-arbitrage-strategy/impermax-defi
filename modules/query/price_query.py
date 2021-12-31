#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 12/26/21 12:29 PM
# @Author   : Benedict
# @File     : price_query.py
# @Desc     : This module is used to query the price of a crypto

#%%
import ccxt
#%% Base class
class PriceQueryBase:
    def __init__(self, exchange_id: str, timeout = 30000, enableRateLimit = True):  #, currency
#         self.currency = currency
        self.exchange_id = exchange_id
        self.timeout = timeout
        self.enableRateLimit = enableRateLimit
#         self.adapt() 
        

#     def adapt(self):
#         self.currency = self.currency.replace("_", "")
    
    def query(self,currency) -> float:
        """
        Query the price of a crypto currency
        :param currency:
        :return:
            the price of the crypto currency in USD/USDC/USDT
        """
        
        exchange_class =getattr(ccxt, self.exchange_id)
        exchange = exchange_class({
        'timeout':self.timeout,
        'enableRateLimit':self.enableRateLimit,
        })
        
        ticker_name = exchange.fetch_ticker(currency)
        name_price = float(ticker_name['last'])
        print(name_price)
#%% choose exchange id
lbank = PriceQueryBase('lbank')
#%% query price output
print(lbank.query("SOLAR/USDT"))
print(lbank.query("SUSHI/USDT"))
# %%
