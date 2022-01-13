#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/1/9 下午3:11
# @Author   : Benedict
# @File     : erc20
# @Desc     : The conctract to call ERC20 contracts

from modules.contracts import Contract
from utils import *
from settings import *


class Erc20(Contract):
    def __init__(self, token: str, private_key=PRIVATE_KEY, address=ADDRESS):
        super().__init__(private_key, address)
        self.abi = read_json('abi/erc20.json')
        contract_address = read_token_address(token)
        self.contract = self.web3.eth.contract(address=to_checksum_address(contract_address),
                                               abi=self.abi)

    def get_all_functions(self):
        return self.contract.all_functions()

    def get_balance(self, address: str = None):
        if address is None:
            address = self.address
        return self.web3.fromWei(self.contract.functions.balanceOf(address).call(), "ether")


if __name__ == '__main__':
    solar = Erc20(PRIVATE_KEY, ADDRESS, 'SOLAR')
    print(solar.get_balance())
