import hashlib
import json
import os
from time import time

BLOCKCHAIN_DIR = os.curdir + '/blocks/'


def check_blocks_integrity():
    result = list()
    cur_proof = - 1
    for i in range(2, int(get_next_block())):
        prev_index = str(i - 1)
        cur_index = str(i)
        tmp = {'block': '', 'result': '', 'proof': ''}
        try:
            file_dict = json.load(open(BLOCKCHAIN_DIR + cur_index + '.json'))
            cur_hash = file_dict['prev_hash']
            cur_proof = file_dict['proof']
        except Exception as e:
            print(e)

        try:
            prev_hash = hashlib.sha256(open(BLOCKCHAIN_DIR + prev_index + '.json', 'rb').read()).hexdigest()
        except Exception as e:
            print(e)

        tmp['block'] = prev_index
        tmp['proof'] = cur_proof
        if cur_hash == prev_hash:
            tmp['result'] = 'ok'
        else:
            tmp['result'] = 'error'
        result.append(tmp)
    return result


def check_block(index):
    cur_index = str(index)
    prev_index = str(int(index) - 1)
    cur_proof = - 1
    cur_hash = 0
    prev_hash = 0
    tmp = {'block': '', 'result': '', 'proof': ''}
    try:
        file_dict = json.load(open(BLOCKCHAIN_DIR + cur_index + '.json'))
        cur_hash = file_dict['prev_hash']
        cur_proof = file_dict['proof']
    except Exception as e:
        print(e)
    try:
        prev_hash = hashlib.sha256(open(BLOCKCHAIN_DIR + prev_index + '.json', 'rb').read()).hexdigest()
    except Exception as e:
        print(e)
    tmp['block'] = prev_index
    tmp['proof'] = cur_proof
    if cur_hash == prev_hash:
        tmp['result'] = 'ok'
    else:
        tmp['result'] = 'error'
    return tmp


def get_hash(file_name):
    file_name = str(file_name)
    if not file_name.endswith('.json'):
        file_name += '.json'
    try:
        with open(BLOCKCHAIN_DIR + file_name, 'rb') as file:
            return hashlib.sha256(file.read()).hexdigest()
    except Exception as e:
        print('File "' + file_name + '" does not exist!n', e)


def get_next_block():
    files = os.listdir(BLOCKCHAIN_DIR)
    index_list = [int(file.split('.')[0]) for file in files]
    cur_index = sorted(index_list)[-1]
    next_index = cur_index + 1
    return str(next_index)


def is_valid_proof(last_proof, proof, difficulty):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:difficulty] == '0' * difficulty


def get_POW(file_name, difficulty=1):
    # POW - proof of work
    file_name = str(file_name)
    if file_name.endswith('.json'):
        file_name = int(file_name.split('.')[0])
    else:
        file_name = int(file_name)

    last_proof = json.load(open(BLOCKCHAIN_DIR + str(file_name - 1) + '.json'))['proof']
    proof = 0
    while is_valid_proof(last_proof, proof, difficulty) is False:
        proof += 1
    cur_block = json.load(open(BLOCKCHAIN_DIR + str(file_name) + '.json'))
    cur_block['proof'] = proof
    cur_block['prev_hash'] = get_hash(str(file_name - 1))
    with open(BLOCKCHAIN_DIR + str(file_name) + '.json', 'w') as file:
        json.dump(cur_block, file, indent=4, ensure_ascii=False)


def write_block(text, make_proof=False):
    cur_index = get_next_block()
    prev_index = str(int(cur_index) - 1)
    prev_block_hash = get_hash(prev_index)
    data = {'text': text,
            'prev_hash': prev_block_hash,
            'timestamp': time(),
            'proof': -1,
            'index': cur_index
            }

    with open(BLOCKCHAIN_DIR + cur_index + '.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    if make_proof is True:
        get_POW(str(cur_index))


if __name__ == '__main__':
    # for i in range(10):
    # write_block(str(i),True)
    for i in range(2, 10):
        print(check_block(str(i)))
    print(check_blocks_integrity())
