#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 12/26/21 12:29 PM
# @Author   : Benedict
# @File     : price_query.py
# @Desc     : This module is used to query current bounty of impermax
#%%
from web3 import Web3
from utils import web3obj, read_json, to_checksum_address
import os
import logging

class BountyQuery:
    def __init__(self):
    # def __init__(self, provider_url):
        # self.web3 = self.connect_web3(provider_url)
        # self.abi = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../abi/', 'impermax.json'))
        
        self.web3 = web3obj
        self.abi = read_json('abi/impermax.json')

        self.contract_dict = {'0x899caad2d29eff3b628503a85dae736b5c4d1671':'ETH/MOVR',
                              '0x35e8f2d87821a5149d92833390880f65911ad4d0':'FRAX/MOVR',
                              '0x2748d9d4e7379d5d29ca8887aeff929912ff06d8':'MIM/MOVR',
                              '0x24e19bd8477077b80de25ee7fc9f7a67d89d8009':'WBTC/MOVR'}
        # self.test_contract = self.web3.eth.contract(address=Web3.toChecksumAddress([*self.contract_dict.keys()][0]), abi=open(self.abi).read())
        self.test_contract = self.web3.eth.contract(address=to_checksum_address('0x899caad2d29eff3b628503a85dae736b5c4d1671'), abi=open(self.abi).read())

    def connect_web3(self, provider_url):
        web3 = Web3(Web3.HTTPProvider(provider_url))
        connected = web3.isConnected()
        if connected:
            logging.info("WEB3 - Connected")
        else:
            logging.info("WEB3 - Disconnected")
        return web3

    def get_bounty(self, address):
        impermax_contract = self.web3.eth.contract(address=Web3.toChecksumAddress(address), abi=open(self.abi).read())
        reward = self.web3.fromWei(impermax_contract.functions.getReward().call(), 'ether')
        reinvest_rate = self.web3.fromWei(impermax_contract.functions.REINVEST_BOUNTY().call(), 'ether')
        bounty = round(reward * reinvest_rate, 5)
        return bounty

    def get_all_bounties(self):
        for address in self.contract_dict:
            print(self.contract_dict[address], '=', self.get_bounty(address))
        

#%%
if __name__ == "__main__":
    # query = BountyQuery('https://moonriver.api.onfinality.io/public')
    query = BountyQuery()

    query.get_all_bounties()

    print(f"\nAll Functions in Contract:\n{query.test_contract.all_functions()}\n")
    
# %%
