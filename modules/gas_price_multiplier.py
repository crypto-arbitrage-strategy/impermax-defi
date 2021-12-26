#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 12/26/21 3:31 PM
# @Author   : Benedict
# @File     : gas_fee_multipliers
# @Desc     : This module is used to decide the gas fee multiplier, which means how much additional gas fee
#             should be paid for the transaction.(Using multiplier way)
#             The multiplier is combined with gas_calculator.py as a whole obverser pattern module.


class Subject:
    def __init__(self):
        self.__observers = []

    def add_observer(self, observer):
        self.__observers.append(observer)

    def delete_observer(self, observer):
        self.__observers.remove(observer)

    def notify_observer(self):
        for observer in self.__observers:
            observer.update()


class GasPriceMultiplier(Subject):
    def __init__(self):
        super().__init__()
        self.multiplier = 1

    def set_multiplier(self, multiplier):
        self.multiplier = multiplier
        self.notify_observer()

    def get_multiplier(self):
        return self.multiplier
