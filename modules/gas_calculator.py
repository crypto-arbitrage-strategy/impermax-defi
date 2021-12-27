#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 12/26/21 2:22 PM
# @Author   : Benedict
# @File     : gas_calculator.py

from gas_price_multiplier import GasPriceMultiplier


class Observer(object):
    @staticmethod
    def update():
        print("Observer got notified")


class GasCalculator(Observer):
    def __init__(self, datasource: GasPriceMultiplier):
        self.gas_price = 0
        self.gas_amount = 0
        self.datasource = datasource

    def set_gas_price(self, multiplier: float):
        self.gas_price = self.get_average_gas_price() * multiplier

    def get_average_gas_price(self) -> float:
        """
        Get the average gas price right now on the chain
        :return:
            average gas price
        """
        return 1  # TODO: For testing, we will return 1 for now

    def estimate_gas_amount(self) -> int:
        pass

    def set_estimate_amount(self):
        self.gas_amount = self.estimate_gas_amount() * 1.05  # 5% extra

    def update(self):
        self.set_gas_price(self.datasource.get_multiplier())
        print("GasFeeCalculator got notified: gas_price = {}".format(self.gas_price))

    def get_total_fee(self) -> int:
        return self.gas_amount * self.gas_price


if __name__ == '__main__':
    gpm = GasPriceMultiplier()
    gfc = GasCalculator(gpm)
    gpm.add_observer(gfc)
    gpm.set_multiplier(1.1)
