#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 12/29/21 9:07 PM
# @Author   : Benedict
# @File     : competitors_query.py
# @Desc     : The file that used to detect competitors' strategy

import requests
from settings import *
from typing import List, Union
from modules.error import TransactionsQueryError
from utils import to_checksum_address, read_impermax_pairs_address


class CompetitorsQuery:
    def __init__(self, api_key: str = API_KEY):
        self.api_key = api_key

    def get_recent_transactions(self, pair: str, num: int, address: Union[list, str, None] = None) -> list:
        contract_address = to_checksum_address(read_impermax_pairs_address(pair))
        res = requests.get(
            f'https://api-moonriver.moonscan.io/api?module=account&action=txlist&address={contract_address}&startblock=1&endblock=99999999&sort=asc&apikey={self.api_key}').json()

        if res["status"] == "1":
            print("Successfully get recent transactions")

            if not address:
                res = res["result"][-num:]
                return res
            else:
                if type(address) == str:
                    address = [address.lower()]
                else:
                    address = list(map(lambda x: x.lower(), address))
                res = res["result"]
                res = [x for x in res if x["from"] in address]
                res = res[-num:]
                return res
        else:
            raise TransactionsQueryError("Failed to get recent transactions")

    def get_recent_call_timestamp(self, pair: str, num: int, address: Union[list, str, None] = None) -> List[int]:
        """
        Get the interval of recent transactions in seconds
        :param address:
        :param num:
        :return:
        """
        transactions = self.get_recent_transactions(pair, num, address)
        if transactions:
            timestamp = list(map(lambda x: int(x["timeStamp"]), transactions))
        return timestamp

    def get_recent_call_interval(self, pair: str, num: int, address: Union[list, str, None] = None) -> List[int]:
        """
        Get the interval of recent transactions in seconds
        :param num: number of transactions
        :return: The interval of recent transactions in seconds
        """
        if num <= 1:
            raise ValueError("num should be greater than 1")
        transactions = self.get_recent_call_timestamp(pair, num, address)
        if transactions:
            interval = list(map(lambda x: int(x[1]) - int(x[0]), zip(transactions[:-1], transactions[1:])))
        return interval[::-1]


if __name__ == '__main__':
    cq = CompetitorsQuery("1RMNSD1YRGHX8TUKN5IFRT6NSXVVBQYPCF")
    print(cq.get_recent_call_timestamp("ETH/WMOVR", 1))
