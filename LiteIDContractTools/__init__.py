from ethjsonrpc import EthJsonRpc
from Crypto.Hash import SHA256
import random
import time

class LiteIDContract:
	def __init__(self, ip='127.0.0.1', port=8545, contract_id=None):
		self.connection = EthJsonRpc(ip, port)
		self.contract_id = contract_id
		self.abi_def = [
							{
								"constant": False,
								"inputs": [],
								"name": "dumpSaltedHashArray",
								"outputs": [
									{
										"name": "Hashes",
										"type": "bytes32[]"
									},
									{
										"name": "Salts",
										"type": "bytes32[]"
									},
									{
										"name": "Timestamps",
										"type": "uint256[]"
									}
								],
								"payable": False,
								"type": "function"
							},
							{
								"constant": False,
								"inputs": [
									{
										"name": "Hash",
										"type": "bytes32"
									},
									{
										"name": "Salt",
										"type": "bytes32"
									}
								],
								"name": "addHash",
								"outputs": [],
								"payable": False,
								"type": "function"
							},
							{
								"inputs": [
									{
										"name": "Hash",
										"type": "bytes32"
									},
									{
										"name": "Salt",
										"type": "bytes32"
									}
								],
								"payable": False,
								"type": "constructor"
							}
						]

	def _caculate_hash(self, data):
		salt = bytearray(random.getrandbits(8) for i in range(32))
		origanal_hash = SHA256(data=data)
		salted_hash = SHA256(data=(origanal_hash.digest() + salt))
		salt = (''.join('{:02x}'.format(x) for x in salt)).decode("hex")
		origanal_hash = origanal_hash.hexdigest().decode("hex")
		salted_hash = salted_hash.hexdigest().decode("hex")
		return salted_hash, salt, origanal_hash

	def unlockAccount(self, account, password):
		self.connection._call('personal_unlockAccount',params=[account, password, 36000])

	def addHash(self, data):
		if self.contract_id is None:
			raise IOError
		salted_hash, salt, origanal_hash = self._caculate_hash(data)
		tx = self.connection.call_with_transaction(self.connection.eth_coinbase(),
												self.contract_id,
												'addHash(bytes32,bytes32)',
												[salted_hash, salt])
		print "Waiting for addHash to be mined"
		while self.connection.eth_getTransactionReceipt(tx) is None:
			time.sleep(1)
		return origanal_hash

	def create_contranct(self, data):
		if not hasattr(self,'byte_code'):
			file = open('LiteID-Contranct.sol')
			code_data = self.connection.eth_compileSolidity(file.read())
			self.byte_code = code_data['ID']['code']
			self.abi_def = code_data['ID']['info']['abiDefinition']
		salted_hash, salt, origanal_hash = self._caculate_hash(data)
		tx_id = self.connection.create_contract(self.connection.eth_coinbase(),
												self.byte_code, 300000,
												sig='addHash(bytes32,bytes32)',
												args=[salted_hash, salt])
		print "Waiting for contranct to be mined"
		while self.connection.eth_getTransactionReceipt(tx_id) is None:
			time.sleep(1)
		self.contract_id = self.connection.eth_getTransactionReceipt(tx_id)['contractAddress']
		return self.contract_id

	def dump_hashes(self):
		return_types = list()
		for item in self.abi_def:
			try:
				if item['name'] == 'dumpSaltedHashArray':
					for i in item['outputs']:
						return_types.append(i['type'])
			except KeyError:
				pass
		return_types = ['bytes32[]', 'bytes32[]', 'uint256[]']
		return self.connection.call(self.contract_id, 'dumpSaltedHashArray()', [], return_types)