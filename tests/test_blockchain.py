import json
from time import time
import pytest

from fiblockchain.blockchain import Blockchain


import sys


def test_version():
    assert sys.version_info.major == 3


def test_bc_1():
    blockcain = Blockchain("temp1.bak")

    assert blockcain.chain != []

    # assert len(blockcain.chain) == 1

    assert blockcain.chain[-1] == blockcain.last_block

    # assert blockcain.last_block['index'] == 1
    # assert blockcain.last_block['timestamp'] < time()
    # assert blockcain.last_block['transactions'] == blockcain.current_transactions

    blockcain.new_tansaction('12345', '54321', 1000)
    blockcain.new_tansaction('12345', '54321', 1000)
    blockcain.new_tansaction('12345', '54321', 1000)
    blockcain.new_tansaction('12345', '54321', 1000)

    blockcain.mine(node_identifire="33333")
    blockcain.mine(node_identifire="33333")
    blockcain.mine(node_identifire="33333")
    blockcain.mine(node_identifire="33333")
    blockcain.mine(node_identifire="33333")
    blockcain.mine(node_identifire="33333")
    blockcain.mine(node_identifire="33333")
    blockcain.mine(node_identifire="33333")
    blockcain.mine(node_identifire="33333")
    blockcain.mine(node_identifire="33333")
