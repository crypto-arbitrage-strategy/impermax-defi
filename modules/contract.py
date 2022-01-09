import time
from utils import web3obj, to_checksum_address, read_json
from abc import ABC
from web3 import Web3
from settings import PRIVATE_KEY, ADDRESS


class Contract(ABC):
    def __init__(self, private_key, address):
        self.web3 = web3obj
        self.router_contract = None
        self.private_key = private_key
        self.address = address
        self.token_address = read_json('address/token.json')

    def get_all_functions(self):
        functions = self.router_contract.all_functions()
        return functions
