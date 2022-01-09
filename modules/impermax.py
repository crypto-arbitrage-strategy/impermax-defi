#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 12/26/21 12:29 PM
# @Author   : Benedict
# @File     : transaction.py
# @Desc     : This module is used to send and handle transaction to achieve the interaction between python and contract.

from web3 import Web3, HTTPProvider
from utils import read_json, to_checksum_address, read_impermax_pairs_address
from contract import Contract
from settings import PRIVATE_KEY, ADDRESS
import asyncio
import threading


class Impermax(Contract):
    def __init__(self, private_key, address):
        super().__init__(private_key, address)
        self.abi = read_json('abi/impermax.json')
        contract_address = read_impermax_pairs_address("ETH/MOVR")
        self.contract = self.web3.eth.contract(address=to_checksum_address(contract_address),
                                               abi=self.abi)

    def __str__(self):
        return f"Connected: {self.w3.isConnected()}"



    def reinvest(self, pair: str, nonce: int = None) -> dict:
        """
        This function is used to trigger the reinvest function.
        :param pair: pair eg.ETH/MOVR
        :return:
            if it is successful, return {200:transaction_hash}
            if it is failed, return {400:error}l
        """
        contract_address = read_impermax_pairs_address(pair)
        self.contract = self.web3.eth.contract(address=to_checksum_address(contract_address),
                                               abi=self.abi)

        try:
            if nonce is None:
                nonce = self.web3.eth.get_transaction_count(self.address)
            txn = self.contract.functions.reinvest().buildTransaction({
                'from': self.address,
                'value': 0,
                'gas': 5000000,
                'gasPrice': self.web3.eth.gasPrice,
                'nonce': nonce,
            })
            signed_tx = self.web3.eth.account.sign_transaction(txn, self.private_key)
            txn_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print("Waiting for confirmation")
            txn_receipt = self.web3.eth.wait_for_transaction_receipt(txn_hash)
            res = {200: f'success:{txn_receipt}'}
            print(res)
            return res
        except Exception as e:
            res = {400: e}
            print(res)
            return res

    def reinvest_combo(self, *args):
        """
        This function is used to trigger the reinvest function combo.
        :param args: the pairs to trigger
        :return:
        """
        names = locals()
        nounce = self.web3.eth.get_transaction_count(self.address)
        nounce_list = range(nounce, nounce + len(args))
        for n, name in zip(nounce_list, args):
            names[f"t_{n}"] = threading.Thread(target=self.reinvest, args=(name, n))

        for n, name in zip(nounce_list, args):
            names[f"t_{n}"].start()


if __name__ == '__main__':
    impermax = Impermax(PRIVATE_KEY, ADDRESS)
    # print(impermax.reinvest("FRAX/MOVR"))
    print(impermax.reinvest_combo( "MIM/MOVR","FRAX/MOVR","MIM/MOVR"))
