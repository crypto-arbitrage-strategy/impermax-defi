#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 01/04/22 13:47 PM
# @Author   : Benedict
# @File     : swap.py
import time
from utils import web3obj, to_checksum_address, read_json
from abc import ABC
import web3
from settings import PRIVATE_KEY, ADDRESS


class Swap(ABC):
    def __init__(self, private_key, address):
        self.web3 = web3obj
        self.router_contract = None
        self.private_key = private_key
        self.address = address


class Solarbean(Swap):
    def __init__(self, private_key, address):
        super().__init__(private_key, address)
        router_contract = '0xaa30ef758139ae4a7f798112902bf6d65612045f'
        self.abi = read_json('abi/solarbeam.json')
        self.router_contract = self.web3.eth.contract(address=to_checksum_address(router_contract),
                                                      abi=self.abi)

    def get_all_functions(self):
        functions = self.router_contract.all_functions()
        return functions

    def swap_solar_for_eth(self, amount_in: int,
                           sender_address: str, amount_out_min: int = 0,
                           path: list = ["6bd193ee6d2104f14f94e2ca6efefae561a4334b",
                                         "98878b06940ae243284ca214f92bb71a2b032b8a"],

                           ) -> dict:

        """
        :param sender_address:
        :param amount_in:
        :param amount_out_min:
        :param path:
        :return:
            if it is successful, return {200:transaction_hash}
            if it is failed, return {400:error}
        """
        start = time.time()
        deadline = (start + 100000)
        try:
            amount_in = int(amount_in * 1e18)
            amount_out_min = int(amount_out_min * 1e18)
            nonce = self.web3.eth.get_transaction_count(sender_address)
            txn = self.router_contract.functions.SwapExactTokensForEth(amount_in, amount_out_min, path,
                                                                       deadline=deadline,
                                                                       to=sender_address, ).buildTransaction({
                'from': sender_address,
                'value': self.web3.toWei(amount_in, 'ether'),
                'gas': 50000,
                'gasPrice': self.web3.eth.gasPrice,
                'nonce': nonce,
            })
            signed_txn = self.web3.eth.account.sign_transaction(txn, self.private_key)
            tx_token = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            transaction = (self.web3.toHex(tx_token))
            return {200: f'success: {transaction}'}
        except Exception as e:
            return {400: e}

    # def get_price_input(self,
    #     token0:str, # input token
    #     token1:str,  # output token
    #     qty: int,
    #     fee: int = None,
    # ) -> int:
    #     self.router_contract.functions.SwapExactTokensForEth(amount_in, amount_out_min, path,
    #                                                          deadline=deadline,
    #                                                          to=sender_address, ).call()
    #

if __name__ == '__main__':
    solarbean = Solarbean(PRIVATE_KEY, ADDRESS)
    print(solarbean.get_all_functions())
    print(solarbean.swap_solar_for_eth(amount_in=0.001, sender_address=ADDRESS))
