#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 12/26/21 1:47 PM
# @Author   : Benedict
# @File     : profit.py
from typing import Union, List

from modules.query import BountyQuery
from modules.contracts.swap import Solarbean
from modules.gas_calculator import GasCalculator, Observer
from modules.gas_price_multiplier import GasPriceMultiplier


class Profit(object):
    def __init__(self):
        self.solarbean = Solarbean()
        self.bounty_query = BountyQuery()
        self.gpm = GasPriceMultiplier()
        self.gfc = GasCalculator(self.gpm)
        self.gpm.add_observer(self.gfc)

    def get_profit(self, pairs: Union[list, str]) -> float: #FIXME sushi is not a list
        """
        Get the profit of the given pairs.
        :param pairs: list of pairs
        :param cheating: the cheating pair to call
        :return: profit
        """
        if isinstance(pairs, str):
            bounty = self.bounty_query.get_bounty(pairs)
            bounty_in_eth = self.solarbean.price_query(bounty, "ETH", "SOLAR")
            return bounty_in_eth - self.gfc.get_total_fee()
        else:
            profit = 0
            for pair in pairs:
                bounty = self.bounty_query.get_bounty(pair)
                bounty_in_eth = self.solarbean.price_query(bounty, "ETH", "SOLAR")
                profit += bounty_in_eth - self.gfc.get_total_fee()
            return profit

if __name__ == '__main__':
    p = Profit()
    print(p.get_profit("MIM/MOVR"))