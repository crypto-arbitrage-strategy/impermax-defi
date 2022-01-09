#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 12/26/21 9:07 PM
# @Author   : Benedict
# @File     : base_strategy.py
# @Desc     : The base strategy. When profit is bigger than the threshold, we will tragger the strategy.

from web3 import Web3
import os
from modules import Profit, Impermax
from random import randint
from modules.query import CompetitorsQuery
from modules.contracts import erc20, swap, impermax
from modules.profit import Profit
from settings import *
import time
import multiprocessing as mp


class BaseStrategy:
    def __init__(self, pair=None):
        self.pair = pair
        self.competitors_query = CompetitorsQuery()
        self.erc20_contract = erc20.Erc20("SOLAR")
        self.swap_contract = swap.Solarbean()
        self.profit = Profit()
        self.impermax_contract = impermax.Impermax()
        self.interval = self.get_interval()

    def get_interval(self):
        interval = self.competitors_query.get_recent_call_interval(self.pair, 10,
                                                                   "0x9Ea0Eb775d02E84EcdebBEEC971d4cA47d091FA8")
        self.interval = min(interval) * 0.9
        return self.interval

    def trigger_or_not(self):
        # binary random,probability is 0.7
        if randint(0, 10) > 7:
            return True
        else:
            return False

    def sell_all_token(self):
        # get all token
        token_balance = float(self.erc20_contract.get_balance(ADDRESS))
        # sell all token
        self.swap_contract.swap_exact_tokens_for_eth(amount_in=token_balance, sender_address=ADDRESS,
                                                     in_token='SOLAR', out_token='ETH')

    def trigger_reinvest(self):
        while True:
            recent_transaction = self.competitors_query.get_recent_call_timestamp(self.pair, 1)[0]
            recent_interval = time.time() - recent_transaction
            if recent_interval > self.interval:
                print("Plan to reinvest")
                if self.profit.get_profit(self.pair) > 0:
                    print("Profit is bigger than the threshold, trigger reinvest")
                    if self.trigger_or_not():
                        print("Randomly trigger: True")
                        self.impermax_contract.reinvest(self.pair)
                    else:
                        print("Randomly trigger: False")
                else:
                    print("Profit is smaller than the threshold, do not trigger reinvest")
                print(f"Trigger reinvest in {self.interval} seconds")
                time.sleep(self.interval)
            else:
                print("Not time to reinvest")
                next_interval = self.interval - recent_interval
                print(f"Trigger reinvest in {next_interval} seconds")
                time.sleep(next_interval)


    def trigger_sell_all(self):
        while True:
            if time.localtime().tm_hour == 21:
                print("Start to sell all")
                self.sell_all_token()
            else:
                print("Not time to sell all")
            print(f"Trigger sell all in next day")
            time.sleep(24*60*60)


def reinvest(pair):
    strategy = BaseStrategy(pair)
    strategy.trigger_reinvest()

def sell_all(pair):
    strategy = BaseStrategy(pair)
    strategy.trigger_sell_all()

if __name__ == '__main__':
    # reinvest("ETH/MOVR")
    eth_movr = mp.Process(target=reinvest, args=("ETH/MOVR",))
    frax_movr = mp.Process(target=reinvest, args=("FRAX/MOVR",))
    mim_movr= mp.Process(target=reinvest, args=("MIM/MOVR",))
    wbtc_movr = mp.Process(target=reinvest, args=("WBTC/MOVR",))
    sell_all = mp.Process(target=sell_all,args=("WBTC/MOVR",))
    eth_movr.start()
    frax_movr.start()
    mim_movr.start()
    wbtc_movr.start()
    sell_all.start()
    eth_movr.join()
    frax_movr.join()
    mim_movr.join()
    wbtc_movr.join()
    sell_all.join()
    print("All processes done")