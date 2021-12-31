from web3 import Web3

def to_checksum_address(address):
    address = Web3.toChecksumAddress(address)
    return address


if __name__=="__main__":
    print(to_checksum_address("0x2748d9d4e7379d5d29ca8887aeff929912ff06d8"))
