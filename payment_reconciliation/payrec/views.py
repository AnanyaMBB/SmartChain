from django.shortcuts import render, redirect
from .models import Entity, ProductsList, involvedEntity
from web3 import Web3, HTTPProvider
from eth_account import Account
# or any other provider such as Infura
# provider = HTTPProvider('https://rpc.sepolia.org/')
provider = HTTPProvider('http://127.0.0.1:7545')

w3 = Web3(provider)


private_key = '0xeadb4294da2a39487ba99272172dd936480d4070418afa229a9e5e83fc244eda'
# contract details
abi = """[
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_productID",
				"type": "uint256"
			},
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
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_productID",
				"type": "uint256"
			}
		],
		"name": "deposit",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "_from",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "_to",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "_amount",
				"type": "uint256"
			}
		],
		"name": "PaymentSent",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_productID",
				"type": "uint256"
			},
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
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "entityDelivery",
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
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
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
				"internalType": "uint256",
				"name": "_productID",
				"type": "uint256"
			},
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
				"internalType": "uint256",
				"name": "_productID",
				"type": "uint256"
			},
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
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_productID",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "getPaidAmount",
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
contract_address = '0xb2E223a63D789F54a0a66Df9694a0a9defeAAca4'  # replace with your contract's address

# get contract instance
contract = w3.eth.contract(address=contract_address, abi=abi)

account = Account.from_key(private_key)
nonce = w3.eth.get_transaction_count(account.address)


userId = None
userAddress = None
loggedIn = False
productId = None


def indexPage(request):
    # product = ProductsList.objects.all()
    print(userAddress)
    entity = Entity.objects.filter(address=userAddress)
    involved = None
    product = None
    if len(entity) != 0:
        print(entity)
        involved = involvedEntity.objects.filter(entityID=entity[0].bID)

        product = [(inv.productID, ProductsList.objects.filter(productID=inv.productID)[0].productName, ProductsList.objects.filter(productID=inv.productID)[0].entityID)
                   for inv in involved]
        # product = ProductsList.objects.filter()

    context = {'loggedIn': loggedIn, 'products': product}
    return render(request, 'payrec/index.html', context)


def createProduct(request):
    context = {}

    if request.method == 'POST':
        if request.POST['Product']:
            product = ProductsList(
                productName=request.POST['Product'], entityID=userId)
            product.save()

            product = ProductsList.objects.filter(
                productName=request.POST['Product'])

            involved = involvedEntity(
                productID=product[0].productID, entityID=userId)
            involved.save()

    return render(request, 'payrec/index.html', context)


def registerUser(request):
    page = 'register'
    context = {'page': page}

    if request.method == 'POST':
        entity = Entity(bname=request.POST['business'],
                        address=request.POST['address'],
                        password=request.POST['bPass'])
        entity.save()
    return render(request, 'payrec/home.html', context)


def login(request):
    global userId
    global userAddress
    global loggedIn
    page = 'login'
    context = {'page': page}

    if request.method == 'POST':
        try:
            checkAccount = Entity.objects.get(address=request.POST['address'])

            if (checkAccount != None) and (checkAccount.password == request.POST['bPass']):
                page = None
                userId = checkAccount.bID
                userAddress = checkAccount.address
                loggedIn = True
                return redirect('indexPage')
        except Exception as ex:
            pass
    return render(request, 'payrec/home.html', context)


def logout(request):
    global userId
    global userAddress
    userId = None
    userAddress = None
    context = {'loggedIn': loggedIn}
    return render(request, 'payrec/index.html', context)


def addEntity(request):
    context = {}

    if request.method == 'POST':
        # print(request.POST)
        if request.POST['entityAddress']:
            print(request.POST['entityAddress'])
            # entity = Entity.objects.get(
            #     address=request.POST['entityAddress'])

            # involved = involvedEntity(
            #     productID=productId, entityID=userId)
            # involved.save()
        return redirect('product', )
    return render(request, 'payrec/product.html', context)


def home(request):
    context = {}

    return render(request, 'payrec/home.html', context)


def product(request, pk):
    global productId
    productId = pk

    if request.method == 'POST':
        # print(request.POST)
        if request.POST['entityAddress']:
            print(request.POST['entityAddress'])
            # entity = Entity.objects.get(
            #     address=request.POST['entityAddress'])

            if Entity.objects.filter(
                    address=request.POST['entityAddress']).exists():
                entity = Entity.objects.get(
                    address=request.POST['entityAddress'])
                print(f'====> {productId}')
                involved = involvedEntity(
                    productID=productId, entityID=entity.bID)
                involved.save()
                nonce = w3.eth.get_transaction_count(account.address)
                transaction = {
                    'to': contract_address,
                    'value': 0,  # No ETH transfer
                    'gas': 2000000,  # adjust the gas limit
                    'gasPrice': w3.to_wei('1', 'gwei'),
                    'nonce': nonce,
                    'chainId': 1337,  # Replace SEPOLIA_CHAIN_ID with the actual chain ID of Sepolia
                    'data': contract.encodeABI(fn_name="addPaymentPath", args=[
                        int(productId),
                        userAddress,
                        request.POST['entityAddress'],
                        w3.to_wei(2, 'ether')
                    ]),  # Encode the function and its arguments for the transaction data
                }
                signed_transaction = w3.eth.account.sign_transaction(
                    transaction, private_key)

                # Send the transaction
                tx_hash = w3.eth.send_raw_transaction(
                    signed_transaction.rawTransaction)

                # Wait for transaction to be mined
                receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                print(receipt)

                # Check the amount after adding the payment path

            else:
                print("Entity not found")
        return redirect('product', pk)

    involved = involvedEntity.objects.filter(productID=productId)

    involved = [(inv.entityID, Entity.objects.filter(bID=inv.entityID)[0].bname, Entity.objects.filter(bID=inv.entityID)[0].address, contract.functions.finishedPayment(int(productId), Entity.objects.filter(bID=inv.entityID)[0].address).call())
                for inv in involved]

    amount = contract.functions.getAmount(int(productId), userAddress).call()
    paidAmount = contract.functions.getPaidAmount(
        int(productId), userAddress).call()

    print(f'===> {amount}')
    print(paidAmount // 1e18)

    context = {'loggedIn': loggedIn, 'pk': pk,
               'involvedEntities': involved, 'amount': (amount // 1e18 - (paidAmount // 1e18))}
    return render(request, 'payrec/product.html', context)
