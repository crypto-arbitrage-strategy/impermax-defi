#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 12/26/21 12:29 PM
# @Author   : Benedict
# @File     : transaction.py
# @Desc     : This module is used to send and handle transaction to achieve the interaction between python and contract.

from web3 import Web3, HTTPProvider


class Transaction:
    def __init__(self, w3: HTTPProvider, contract_address: str, contract_abi: list, private_key: str):
        self.w3 = w3
        self.contract_address = contract_address
        self.contract_abi = contract_abi
        self.private_key = private_key

    def __str__(self):
        return f"Connected: {self.w3.isConnected()}"

    def trigger_transaction(self) -> dict:
        """
        This function is used to trigger the transaction.
        :return:
            if it is successful, return {200:transaction_hash}
            if it is failed, return {400:error}l
        """
        pass
