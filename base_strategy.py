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
from modules.error import TransactionsQueryError


class BaseStrategy:
    def __init__(self, pair=None):
        self.pair = pair
        self.competitors_query = CompetitorsQuery()
        self.erc20_contract = erc20.Erc20("SOLAR")
        self.swap_contract = swap.Solarbean()
        self.profit = Profit()
        self.impermax_contract = impermax.Impermax()
        self.competitors_address_set = {"0x9ea0eb775d02e84ecdebbeec971d4ca47d091fa8",
                                        "0xcc25Bcbe08E12E62113add458dE3b9375A511b63"}
        self.interval = self.get_interval()


    # def update_competitors_address(self):
    #     self.competitors_address_set
    #     new_competitors_address_set = self.competit

    def get_interval(self):
        try:
            interval = self.competitors_query.get_recent_call_interval(self.pair, 10,self.competitors_address_set)
            self.interval = min(list(filter(lambda x: x > 30, interval)))
            # if recent three transactions are triggered by me, we will increase by 1.1

            recent_address_set = set(
                i["from"] for i in self.competitors_query.get_recent_transactions(self.pair, 3))
            self.competitors_address_set = self.competitors_address_set.union(recent_address_set) - {ADDRESS}
            if recent_address_set == {ADDRESS}:
                self.interval *= 1.1
            else:
                self.interval = self.interval * 0.9
            return self.interval
        except TransactionsQueryError as e:
            time.sleep(1)
            print(e)
            self.get_interval()  # try again

    def trigger_or_not(self):
        # binary random,probability is 0.7
        # if randint(0, 10) >= 3:
        #     return True
        # else:
        #     return False
        return True

    def cheating_or_not(self):
        try:
            if "0x5d57D72EeEd82fc8cfce9ad9925e5bB2513b3107" not in set(
                    i["from"] for i in self.competitors_query.get_recent_transactions("ETH/WMOVR", 3)):
                return False
            else:
                return True
        except TransactionsQueryError as e:
            time.sleep(1)
            print(e)
            self.cheating_or_not()  # try again

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
            self.get_interval()
            print(f"get new interval: {self.interval}")
            if recent_interval > self.interval:
                print("Plan to reinvest")
                if self.profit.get_profit(self.pair) > 0.00004:
                    print("Profit is bigger than the threshold, trigger reinvest")
                    if self.trigger_or_not():
                        print("Randomly trigger: True")
                        if self.cheating_or_not():  # decide whether to cheat
                            if self.pair != "FRAX/MOVR":
                                self.impermax_contract.reinvest_combo("FRAX/MOVR", self.pair)
                            else:
                                self.impermax_contract.reinvest(self.pair)
                        else:
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
                next_interval = min(1200, next_interval)
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
            time.sleep(24 * 60 * 60)


def reinvest(pair):
    strategy = BaseStrategy(pair)
    strategy.trigger_reinvest()


def sell_all(pair):
    strategy = BaseStrategy(pair)
    strategy.trigger_sell_all()


if __name__ == '__main__':
    # reinvest("MIM/MOVR")
    eth_movr = mp.Process(target=reinvest, args=("ETH/MOVR",))
    frax_movr = mp.Process(target=reinvest, args=("FRAX/MOVR",))
    mim_movr = mp.Process(target=reinvest, args=("MIM/MOVR",))
    wbtc_movr = mp.Process(target=reinvest, args=("WBTC/MOVR",))
    sell_all = mp.Process(target=sell_all, args=("WBTC/MOVR",))
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
