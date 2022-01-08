#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 12/26/21 12:29 PM
# @Author   : Benedict
# @File     : price_query.py
# @Desc     : This module is used to query the price of a crypto

#%%
from utils import web3obj, to_checksum_address, read_json
from abc import ABC
from web3 import Web3
from settings import PRIVATE_KEY, ADDRESS

#%%
class Query():
    def __init__(self, private_key, address):
        self.web3 = web3obj 
        self.router_contract = None 
        self.private_key = private_key
        self.address = address
        self.abi = read_json('solarbeam.json')
        contract = '0xaa30ef758139ae4a7f798112902bf6d65612045f'
        self.contract = self.web3.eth.contract(address=to_checksum_address(contract),abi=self.abi)
        
        basetoken = '0x98878B06940aE243284CA214f92Bb71a2b032B8A' #WETH
        selltoken = '0x6bD193Ee6D2104F14F94E2cA6efefae561A4334B' #SOLAR
        self.basetoken = basetoken
        self.selltoken = selltoken


    
    def price_query(self,amount_in) -> float:
        """
        Query the price of a crypto currency
        :param currency:
        :return:
            the price of the crypto currency in movr
        """
        baseCurrency = self.web3.toChecksumAddress(self.basetoken)    #MOVR or WETH
        tokenToSell = self.web3.toChecksumAddress(self.selltoken)     #SOLAR

        #Calculate minimum amount of tokens to receive
        amountOut = self.contract.functions.getAmountsOut(10**18, [tokenToSell, baseCurrency],fee=30).call()
        amountOutMin = amount_in * float((self.web3.fromWei(int(amountOut[1]),'ether')))
        return amountOutMin #Minimum tokens to recieve


#%%
if __name__ == '__main__':
    Query = Query(PRIVATE_KEY, ADDRESS)
    print(Query.price_query(amount_in=1.3))

