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
        try:
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
        except requests.exceptions.ConnectionError:
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
        else:
            timestamp = [1645187040, 1645188372, 1645189716, 1645191036, 1645192374, 1645193718, 1645195038, 1645196346, 1645197720, 1645199082]
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
    a = cq.get_recent_call_timestamp("ETH/MOVR",10)
    # print(min(list(filter(lambda x: x > 0, a))))
    print(a)