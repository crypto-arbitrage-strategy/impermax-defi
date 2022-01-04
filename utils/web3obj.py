#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 12/26/21 3:31 PM
# @Author   : Benedict
# @File     : gas_fee_multipliers
# @Desc     : This module is used to initialize the web3 object

from web3 import Web3

web3obj = Web3(Web3.HTTPProvider('https://moonriver.api.onfinality.io/public'))

web3obj.eth.estimate_gas({'to': '0x2748d9d4e7379d5d29ca8887aeff929912ff06d8', 'from':'0xa037df5216908cB1353D634306C88cb4Fc662BAc', 'value': 0})
