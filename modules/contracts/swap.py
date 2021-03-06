#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 01/04/22 13:47 PM
# @Author   : Benedict
# @File     : swap.py
import time
from utils import web3obj, to_checksum_address, read_json,read_token_address
from abc import ABC
from web3 import Web3
from settings import PRIVATE_KEY, ADDRESS
from modules.contracts import Contract


class Solarbean(Contract, ABC):
    def __init__(self, private_key=PRIVATE_KEY, address=ADDRESS):
        super().__init__(private_key, address)
        router_contract = '0xaa30ef758139ae4a7f798112902bf6d65612045f'
        self.abi = read_json('abi/solarbeam.json')
        self.contract = self.web3.eth.contract(address=to_checksum_address(router_contract),
                                               abi=self.abi)


    # TODO: add aprrove function, right now we need to approve it manually
    def swap_exact_tokens_for_eth(self, amount_in: int,
                                  sender_address: str,
                                  out_token: str,
                                  in_token: str,
                                  # path: list = [Web3.toChecksumAddress("98878b06940ae243284ca214f92bb71a2b032b8a"),
                                  #               Web3.toChecksumAddress("6bd193ee6d2104f14f94e2ca6efefae561a4334b"),
                                  #               ],
                                  amount_out_min: int = 0,

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
            path = [Web3.toChecksumAddress(self.token_address[in_token]),
                    Web3.toChecksumAddress(self.token_address[out_token])]
            txn = self.contract.functions.swapExactTokensForETH(amount_in, amount_out_min, path,
                                                                to=sender_address,
                                                                deadline=int(deadline),
                                                                ).buildTransaction({
                'from': sender_address,
                'value': 0,
                'gas': 500000,
                'gasPrice': self.web3.eth.gasPrice,
                'nonce': nonce,
            })
            signed_tx = self.web3.eth.account.sign_transaction(txn, self.private_key)
            txn_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print("Waiting for confirmation")
            txn_receipt = self.web3.eth.wait_for_transaction_receipt(txn_hash)
            res = {200: f'success: {txn_receipt}'}
            print(res)
            return res
        except Exception as e:
            res = {400: f'error: {e}'}
            print(res)
            return res

    def price_query(self, amount_in,base_token,sell_token) -> float:
        """
        Query the price of a crypto currency
        :param currency:
        :return:
            the price of the crypto currency in movr
        """
        base_token_address = read_token_address(base_token)
        sell_token_address = read_token_address(sell_token)
        baseCurrency = self.web3.toChecksumAddress(base_token_address)
        tokenToSell = self.web3.toChecksumAddress(sell_token_address)
        # Calculate minimum amount of tokens to receive
        amountOut = self.contract.functions.getAmountsOut(10 ** 18, [tokenToSell, baseCurrency], fee=30).call()
        amountOutMin = amount_in * float((self.web3.fromWei(int(amountOut[1]), 'ether')))
        return amountOutMin  # Minimum tokens to recieve


if __name__ == '__main__':
    solarbean = Solarbean(PRIVATE_KEY, ADDRESS)
    print(solarbean.price_query(1, "ETH", "SOLAR"))
    # print(
    #     solarbean.swap_exact_tokens_for_eth(amount_in=0.01, sender_address=ADDRESS, in_token='SOLAR', out_token='MOVR'))
