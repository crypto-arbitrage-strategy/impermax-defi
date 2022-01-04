#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 12/26/21 9:07 PM
# @Author   : Benedict
# @File     : base_strategy.py
# @Desc     : The base strategy. When profit is bigger than the threshold, we will tragger the strategy.

from web3 import Web3
import os
from modules import Profit, Transaction


class BaseStrategy:  # the prototype of strategy, without considering other participants
    def __init__(self, web3: Web3, contract_address: str, contract_abi: list, threshold: int, profit: Profit):
        private_key = os.environ.get('PRIVATE_KEY')  # get private key from env
        self.transaction = Transaction(web3, contract_address, contract_abi, private_key)
        self.threshold = threshold
        self.profit = profit

    def run(self):
        if self.profit.get_profit() > self.threshold:
            self.transaction.trigger()
