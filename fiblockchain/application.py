# coding: utf-8
import json
from flask import Flask, Response, request, jsonify
from uuid import uuid4
from fiblockchain.blockchain import Blockchain


# Flask APP
app = application = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# (global) ノードのユニークなアドレスを作成
node_identifire = str(uuid4()).replace('-', '')
# blockchain = Blockchain()
blockchain = Blockchain("blockchain.bak")


@app.route("/test", methods=["GET"])
def test():
    return Response(json.dumps({'Output': 'Hello Test'}), mimetype='application/json', status=200)


@app.route("/test", methods=['POST'])
def test_post():
    data = {"Output": "Hello Test"}
    return Response(json.dumps(data), mimetype='application/json', status=200)


@app.route('/transactions/new', methods=['POST'])
def new_transactions():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.new_tansaction(
        values['sender'],
        values['recipient'],
        values['amount'])

    response = {'message': f'トランザクションはブロック{index}に追加されました',
                'Output': 'Hello Test'
                }
    return jsonify(response)
    # return Response(json.dumps(response), mimetype='application/json', status=200)


@app.route('/mine', methods=['GET'])
def mine():
    # 次のプルーフを見つけるためのプルーフオブワークアルゴリズムを使用
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # プルーフを見つけたことに対する報酬を得る
    # 送信者は採掘者が新しいコインを採掘したことを表すために"0"とする
    blockchain.new_tansaction(
        sender="0",
        recipient=node_identifire,
        amount=1,
    )

    # チェーンに新しいブロックを加えることで、新しいブロックを採掘する
    block = blockchain.new_block(proof)

    # マイニングした結果をユーザに返す
    response = {
        'message': '新しいブロックを採掘しました',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_node():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: 有効ではないノードのリストです", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': '新しいノードが追加されました',
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'チェーンが置き換えられました',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'チェーンが確認されました',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == "__main__":
    import sys
    # print("[EXAMPLE] python application.py 0.0.0.0 8000")
    host = sys.argv[1]
    port = sys.argv[2]
    # print(sys.argv)
    # app.run(host="0.0.0.0", port=8000, debug=True)
    app.run(host, port, True)
