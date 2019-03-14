from flask import Flask, jsonify, request
import json
from uuid import uuid1
from blockchain_test import Blockchain

app = Flask(__name__)
blockchain = Blockchain()
node_id = str(uuid1())

@app.route('/mine', methods=['GET'])
def mine():
	blockchain.new_transaction(
		sender="0",
		recipient=node_id,
		amount=1
	)
	block = blockchain.new_block()
	return jsonify({
		'id': block['id'], 
		'proof': block['proof'], 
		'transactions': block['transactions'], 
		'prev_hash': block['prev_hash']}), 200

@app.route('/chain', methods=['GET'])
def show_chain():
	return jsonify(blockchain.chain), 200

@app.route('/trans/new', methods=['POST'])
def new_trans():
	values = request.get_json()
	index = blockchain.new_transaction(
		values['sender'], 
		values['recipient'], 
		values['amount'])
	return jsonify({'msg': f'Transaction at index {index}'}), 200

@app.route('/nodes/new', methods=['POST'])
def new_nodes():
	values = request.get_json()
	for node in values['nodes']:
		blockchain.new_node(node)
	return jsonify({'msg': 'New nodes!', 'nodes': list(blockchain.nodes)}), 200

@app.route('/nodes/solve', methods=['GET'])
def consensus():
	return jsonify({'msg': 'Chain replaced!' if blockchain.consensus() else 'Authoritarian chain',
	 'chain': blockchain.chain})

if __name__ == '__main__':
	port = int(input("Type port number: "))
	app.run(host='0.0.0.0', port=port)