from hashlib import sha256
from json import dumps
from time import ctime
from urllib.parse import urlparse
from requests import get


class Blockchain:
	def __init__(self):
		self.chain = []
		self.cur_transactions = []
		self.nodes = set()
		self.new_block(1, 1)

	def new_block(self, proof=None, prev_hash=None):
		block = {
			'id': len(self.chain) + 1, 
			'timestamp': ctime(), 
			'proof': proof or self.validate_proof(), 
			'prev_hash': prev_hash or self.hash(self.last_block), 
			'transactions': self.cur_transactions
		}
		self.chain.append(block)
		self.cur_transactions = []
		return block

	def new_transaction(self, sender, recipient, amount):
		self.cur_transactions.append({
			'sender': sender, 
			'recipient': recipient, 
			'amount': amount
		})
		return self.last_block['id']

	def new_node(self, addr):
		parsed = urlparse(addr).netloc
		if parsed != '':
			self.nodes.add(parsed)

	def validate_chain(self, chain):
		last_block = chain[0]

		for block in chain[1:len(chain)]:
			if block['prev_hash'] != self.hash(last_block):
				return False
			last_block = block
		return True

	def consensus(self):
		new_chain = None
		max_len = len(self.chain)

		for node in self.nodes:
			response = get(
				f'http://{node}/chain', 
				headers={'Content-Type': 'application/json'}
			)
			if response.ok and len(response.json()) > max_len and self.validate_chain(response.json()):
				new_chain = response.json()
				max_len = len(response.json())
		if new_chain:
			self.chain = new_chain
			return True
		return False

	def validate_proof(self):
		proof = 0
		while True:
			if self.hash(f"{self.last_block['proof']}{proof}")[:1] == 'a':
				return proof
			proof += 1

	@staticmethod
	def hash(block):
		return sha256(dumps(block, sort_keys=True).encode()).hexdigest()

	@property
	def last_block(self):
		return self.chain[-1]


if __name__ == '__main__':
	x = Blockchain()
	for i in range(40):
		print(x.new_block())
	print(x.validate_chain(x.chain))