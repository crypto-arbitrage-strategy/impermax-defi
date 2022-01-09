#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 12/26/21 1:47 PM
# @Author   : Benedict
# @File     : profit.py

from .query import bounty_query, price_query
from .gas_calculator import GasCalculator


class Profit(object):
    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity

    def get_profit(self, base_token: str = "usdt") -> float:
        """
        Calculate the profit based on the base token
        :param base_token: default usdt
        :return: profit
        """
        price = price_query(base_token)
        bonus = bounty_query(base_token)
        profit = (self.price - price) * self.quantity * bonus
        return profit
