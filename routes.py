from flask import Flask, jsonify, request, render_template, redirect
from uuid import uuid1
from blockchain import Blockchain

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
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
	return redirect('/chain'), 200

@app.route('/chain', methods=['GET'])
def show_chain():
	try:
		if request.headers['Content-Type'] == 'application/json':
			return jsonify(blockchain.chain)
		else:
			raise KeyError
	except KeyError:
		return render_template('show_chain.html', chain=blockchain.chain)

@app.route('/trans/new', methods=['POST'])
def new_trans():
	values = request.get_json()
	index = blockchain.new_transaction(
		values['sender'], 
		values['recipient'], 
		values['amount'])
	return jsonify({'msg': f'Transaction at index {index}'}), 200

@app.route('/nodes/new', methods=['GET'])
def new_nodes():
	try:
		values = request.args.get('nodes')
		for node in values.split(','):
			blockchain.new_node(node)
		raise AttributeError
	except AttributeError:
		print(list(blockchain.nodes))
		return render_template('nodes.html', nodes=list(blockchain.nodes)), 200

@app.route('/nodes/solve', methods=['GET'])
def consensus():
	return jsonify({
		'msg': 'Chain replaced!' if blockchain.consensus() else 'Authoritarian chain',
		 'chain': blockchain.chain
	 })

if __name__ == '__main__':
	#port = int(input("Type port number: "))
	app.run(host='0.0.0.0', debug=True)