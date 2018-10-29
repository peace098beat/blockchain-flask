# coding: utf-8
import hashlib
import json
from time import time
from pathlib import Path
from urllib.parse import urlparse


"""
block = {
    'index': 1,
    'timestamp': 1506057125.900785,
    'transactions': [
        {
            'sender': "8527147fe1f5426f9dd545de4b27ee00",
            'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
            'amount': 5,
        }
    ],
    'proof': 324984774000,
    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}
"""


class Blockchain(object):

    def __init__(self, backupfile=None):

        self.chain = []
        self.current_transactions = []

        self.nodes = set()

        # ブロックチェーンローカルファイルパス
        if backupfile == None:
            self.backupfile = "tmpolary.bak"
            self.new_block(previous_hash=1, proof=100)
        else:
            self.backupfile = backupfile

            # ジェネシスブロックを作る
            if(Path(self.backupfile).exists()):
                self.load()
            else:
                self.new_block(previous_hash=1, proof=100)

    def load(self):

        import os
        if os.path.getsize(self.backupfile) > 0:
            with open(self.backupfile, 'r') as fp:
                self.chain = json.load(fp)
        else:
            self.chain = []

    def save(self):
        with open(self.backupfile, 'w') as fp:
            json.dump(self.chain, fp, indent=4)

    @property
    def last_block(self):
        return self.chain[-1]

    def new_block(self, proof, previous_hash=None):
        """
        ブロックチェーンに新しいブロックをつくる
        :param proof: <int> プルーフオブワークアルゴリズムからえられるプルーフ
        :param previous_hash: (オプション) <str> 前のブロックハッシュ
        :return: <dict>新しい部ロク
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # 現在のトランザクションをリセット
        self.current_transactions = []

        # ブロックを追加
        self.chain.append(block)

        # 保存
        self.save()

        return block

    def new_tansaction(self, sender, recipient, amount):
        """
        次に採掘されるブロックに加える新しいトランザクションをつくる
        :param sender: <str> 送信者のアドレス
        :param recipient: <str> 受信者のアドレス
        :param amount: <int> 量
        :return: <int> このトランザクションを含むブロックのアドレス
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        ブロックのSHA-256ハッシュを作る
        :param block: <dict> ブロック
        :return: <str>
        """

        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        シンプルなプルーフオブワークのアルゴリズム
         - hash(pp')の最初の4つが0となるようなp'を探す
         - pは1つ前のブロックのプルーフ, p'は新しいブロックのプルーフ
        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        プルーフが正しいかをかくにんする. hash(last_proof, proof)の最初の4つが0となっているか

        """

        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == "0000"

    def mine(self, node_identifire):
        # 次のプルーフを見つけるためのプルーフオブワークアルゴリズムを使用
        last_proof = self.last_block['proof']
        proof = self.proof_of_work(last_proof)

        # プルーフを見つけたことに対する報酬を得る
        # 送信者は採掘者が新しいコインを採掘したことを表すために"0"とする
        self.new_tansaction(
            sender="0",
            recipient=node_identifire,
            amount=1,
        )

        # チェーンに新しいブロックを加えることで、新しいブロックを採掘する
        block = self.new_block(proof)

        return block

    def register_node(self, address):
        """
        ノードリストに新しいノードを加える
        :param address: <str> 例 'http://192.168.0.5:5000'
        return None
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        """
        ブロックチェーンが正しいかを確認する
        :param chain: <list> ブロックチェーン
        :return: <bool> 
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            print(f'{last_block}')
            print(f'{block}')
            print("¥n---------------¥n")

            # ブロックのハッシュが正しいかを確認
            if block['previous_hash'] != self.hash(last_block):
                return False

            # プルーフオブワークが正しいか確認
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block

            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        これがコンセンサスアルゴリズムだ。
        ネットワーク上のもっとも長いチェーンで
        自らのチェーンを置き換えることでコンフリクトを解消する
        :return: <bool> 自らのチェーンが置き換えられると:True. 
        """

        neighbours = self.nodes
        new_chain = None

        # 自らのチェーンより長いチェーンを探す必要がある
        max_length = len(self.chain)

        # ----------------------------------
        # 他のすべてのノードのチェーンを確認
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if not self.valid_chain(chain):
                    continue

                # そのチェーンがより長いか、有効かを確認
                if length > max_length:
                    max_length = length
                    new_chain = chain
        # ---------------------------
        # もし自らのチェーンより長く
        # 有効なチェーンを見つけた場合それで置き換える
        if new_chain:
            self.chain = new_chain
            return True
        # -------------

        return False
