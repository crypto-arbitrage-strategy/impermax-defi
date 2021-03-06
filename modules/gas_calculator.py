#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 12/26/21 2:22 PM
# @Author   : Benedict
# @File     : gas_calculator.py
import web3.contract

from modules.gas_price_multiplier import GasPriceMultiplier
from utils.web3obj import web3obj
from utils import to_checksum_address


class Observer(object):
    @staticmethod
    def update():
        print("Observer got notified")


class GasCalculator(Observer):
    def __init__(self, datasource: GasPriceMultiplier, web3=web3obj):
        self.gas_amount = 500000
        self.datasource = datasource
        self.web3 = web3
        self.gas_price = self.get_average_gas_price()

    def set_gas_price(self, multiplier: float):
        self.gas_price = self.get_average_gas_price() * multiplier

    def get_average_gas_price(self) -> float:
        """
        Get the average gas price right now on the chain
        :return:
            average gas price
        """
        gas_price = self.web3.eth.gasPrice
        return gas_price

    @staticmethod
    def estimate_gas_amount() -> int:  # TODO write a function a estimate the gas amount
        return 500000

    def set_estimate_amount(self):
        self.gas_amount = self.estimate_gas_amount() * 1.05  # 5% extra

    def update(self):
        self.set_gas_price(self.datasource.get_multiplier())
        print("GasFeeCalculator got notified: gas_price = {}".format(self.gas_price))

    def get_total_fee(self) -> int:
        return float(self.web3.fromWei(self.gas_amount * self.gas_price,"ether"))


if __name__ == '__main__':
    gpm = GasPriceMultiplier()
    gfc = GasCalculator(gpm)
    gpm.add_observer(gfc)
    print(gfc.get_total_fee())