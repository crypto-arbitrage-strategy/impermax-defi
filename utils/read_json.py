import json


def read_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def read_impermax_pairs_address(pair: str) -> str:
    return read_json('address/contracts.json')["IMPERMAX"][pair]["address"]


def read_token_address(token: str) -> str:
    return read_json('address/token.json')[token]


if __name__ == '__main__':
    print(read_token_address('SOLAR'))
