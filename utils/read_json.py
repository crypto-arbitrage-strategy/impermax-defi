import json


def read_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


if __name__ == '__main__':
    print(read_json('abi/solarbeam.json'))
