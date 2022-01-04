#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 12/29/21 9:07 PM
# @Author   : Benedict
# @File     : competitors_query.py
# @Desc     : The file that used to detect competitors' strategy

import requests
from typing import List
from modules.error import TransactionsQueryError
from utils import to_checksum_address


class CompetitorsQuery:
    def __init__(self, address: str, api_key: str):
        self.address = to_checksum_address(address)
        self.api_key = api_key
        self.res = requests.get(
            f'https://api-moonriver.moonscan.io/api?module=account&action=txlist&address={address}&startblock=1&endblock=99999999&sort=asc&apikey={api_key}').json()

    def get_recent_transactions(self, num: int) -> list:
        if self.res["status"] == "1":
            print("Successfully get recent transactions")
            return self.res["result"][-num:]
        else:
            raise TransactionsQueryError("Failed to get recent transactions")

    def get_recent_call_timestamp(self, num: int) -> List[int]:
        """
        Get the interval of recent transactions in seconds
        :param num:
        :return:
        """
        transactions = self.get_recent_transactions(num)
        if transactions:
            timestamp = list(map(lambda x: x["timeStamp"], transactions))
        return timestamp

    def get_recent_call_interval(self, num: int) -> List[int]:
        """
        Get the interval of recent transactions in seconds
        :param num: number of transactions
        :return: The interval of recent transactions in seconds
        """
        if num <= 1:
            raise ValueError("num should be greater than 1")
        transactions = self.get_recent_call_timestamp(num)
        if transactions:
            interval = list(map(lambda x: int(x[1]) - int(x[0]), zip(transactions[:-1], transactions[1:])))
        return interval


if __name__ == '__main__':
    cq = CompetitorsQuery("0x2748d9d4e7379d5d29ca8887aeff929912ff06d8", "1RMNSD1YRGHX8TUKN5IFRT6NSXVVBQYPCF")
    print(cq.get_recent_call_interval(10))
