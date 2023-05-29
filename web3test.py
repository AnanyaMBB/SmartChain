from web3 import Web3, HTTPProvider
from eth_account import Account
# or any other provider such as Infura
provider = HTTPProvider('https://rpc.sepolia.org/')
w3 = Web3(provider)


private_key = 'a46f7c9dd0b5a0d52cdfc32515e855391f5abb99ef5355ff0e3827e14d16ef0b'
# contract details
abi = """[
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_from",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "_to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_deliveryStage",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_amount",
				"type": "uint256"
			}
		],
		"name": "addPaymentPath",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "deposit",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_deliveryStage",
				"type": "uint256"
			}
		],
		"name": "sendPayments",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "entityTotal",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "finishedPayment",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "getAmount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]"""  # replace with your contract's ABI
contract_address = '0x57B86A01e147ddA6558cEE37b39b2Fc859b55b8C'  # replace with your contract's address

# get contract instance
contract = w3.eth.contract(address=contract_address, abi=abi)

account = Account.from_key(private_key)
nonce = w3.eth.get_transaction_count(account.address)
print(w3.is_connected)
# Build a transaction
# Build a transaction
# Build a transaction
transaction = {
    'to': contract_address,
    'value': 0,  # No ETH transfer
    'gas': 3000000,  # adjust the gas limit
    'gasPrice': w3.to_wei('1', 'gwei'),
    'nonce': nonce,
    'chainId': 11155111,  # Replace SEPOLIA_CHAIN_ID with the actual chain ID of Sepolia
    'data': contract.encodeABI(fn_name="addPaymentPath", args=[
        '0xB4B256B2f55a6c73c358803E48e5856b1D02eBC8',
        '0xB4B256B2f55a6c73c358803E48e5856b1D02eBC8',
        1,
        20
    ]),  # Encode the function and its arguments for the transaction data
}

# Sign the transaction
# Sign the transaction
signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)

# Send the transaction
tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

# Wait for transaction to be mined
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(receipt)

# Check the amount after adding the payment path
amount = contract.functions.getAmount(
    '0xB4B256B2f55a6c73c358803E48e5856b1D02eBC8').call()
print(amount)
# # add payment path
# _tx = contract.functions.addPaymentPath('0xB4B256B2f55a6c73c358803E48e5856b1D02eBC8', '0xB4B256B2f55a6c73c358803E48e5856b1D02eBC8', 1, 100).buildTransaction({
#     'from': w3.eth.accounts[0],
#     'gas': 70000,
#     'gasPrice': w3.toWei('1', 'gwei'),
#     'nonce': w3.eth.getTransactionCount(w3.eth.accounts[0])
# })

# signed_tx = w3.eth.account.signTransaction(_tx, private_key='YourPrivateKey')
# w3.eth.sendRawTransaction(signed_tx.rawTransaction)

# # check total amount
# total = contract.functions.getAmount('0xAddress1').call()
# print(total)

# # deposit ether
# _tx = contract.functions.deposit().buildTransaction({
#     'from': w3.eth.accounts[0],
#     'value': w3.toWei('1', 'ether'),
#     'gas': 70000,
#     'gasPrice': w3.toWei('1', 'gwei'),
#     'nonce': w3.eth.getTransactionCount(w3.eth.accounts[0])
# })

# signed_tx = w3.eth.account.signTransaction(_tx, private_key='YourPrivateKey')
# w3.eth.sendRawTransaction(signed_tx.rawTransaction)

# # check payment status
# is_finished = contract.functions.finishedPayment('0xAddress1').call()
# print(is_finished)

# # send payments
# _tx = contract.functions.sendPayments(1).buildTransaction({
#     'from': w3.eth.accounts[0],
#     'gas': 70000,
#     'gasPrice': w3.toWei('1', 'gwei'),
#     'nonce': w3.eth.getTransactionCount(w3.eth.accounts[0])
# })

# signed_tx = w3.eth.account.signTransaction(_tx, private_key='YourPrivateKey')
# w3.eth.sendRawTransaction(signed_tx.rawTransaction)
