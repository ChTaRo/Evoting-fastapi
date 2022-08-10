from turtle import update
from web3 import Web3
from web3 import EthereumTesterProvider
from fastapi import FastAPI 
app = FastAPI()

provider_url = 'https://eth-rinkeby.alchemyapi.io/v2/nzd3qo7YE9BQAs5x4dTkyUVJUyi9u8kQ'
w3 = Web3(Web3.HTTPProvider(provider_url))

abi = '[ { "inputs": [ { "internalType": "string", "name": "_name", "type": "string" } ], "name": "addCandidate", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "string", "name": "_name", "type": "string" }, { "internalType": "string", "name": "customerId", "type": "string" }, { "internalType": "string", "name": "_position", "type": "string" } ], "name": "addUser", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "_index", "type": "uint256" }, { "internalType": "string", "name": "customerId", "type": "string" } ], "name": "chooseCandidate", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "stateMutability": "nonpayable", "type": "constructor" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "previousOwner", "type": "address" }, { "indexed": true, "internalType": "address", "name": "newOwner", "type": "address" } ], "name": "OwnershipTransferred", "type": "event" }, { "inputs": [], "name": "renounceOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "newOwner", "type": "address" } ], "name": "transferOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "candidate", "outputs": [ { "internalType": "string", "name": "candidateName", "type": "string" }, { "internalType": "uint256", "name": "score", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "owner", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "ShowCandidate", "outputs": [ { "components": [ { "internalType": "string", "name": "candidateName", "type": "string" }, { "internalType": "uint256", "name": "score", "type": "uint256" } ], "internalType": "struct eVoting.Candidate[]", "name": "candidates", "type": "tuple[]" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "userAccounts", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "string", "name": "", "type": "string" } ], "name": "userAll", "outputs": [ { "internalType": "string", "name": "userName", "type": "string" }, { "internalType": "string", "name": "position", "type": "string" }, { "internalType": "bool", "name": "isVote", "type": "bool" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "winningCandidateIndex", "outputs": [ { "internalType": "uint256", "name": "winningCandidate", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "winningCandidateName", "outputs": [ { "internalType": "string", "name": "winnerName_", "type": "string" } ], "stateMutability": "view", "type": "function" } ]'
contract_address = '0x2a663900B2c598AE2572a132Ba23B1D3CAB8ed71'
contract_instance = w3.eth.contract(address=contract_address, abi = abi)

#add min acc
address = '0xeC25b117bb210F90C7616314c45C1E5432934925'
privatekey = '72963673a1fad7dd249783f505c00a5c33cdd6ea651218764dacef3c86cc1c51'

@app.get("/")
async def home():
    return {"message": "Hello World"}

@app.get("/addCandidate/{name}")
async def addCandidate(name:str):
    nonce = w3.eth.getTransactionCount(address)
    update_transaction = contract_instance.functions.addCandidate(name).buildTransaction({
        'gas': 1800000,
        'gasPrice': w3.toWei('50', 'gwei'),
        'from': address,
        'nonce': nonce
    })
    sign_transaction = w3.eth.account.sign_transaction(update_transaction, private_key = privatekey)
    transaction_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
    transaction_hash = w3.toHex(transaction_hash)
    return {"hash": transaction_hash}

@app.get("/ShowCandidate")
async def ShowCandidate():
    candidate = contract_instance.functions.ShowCandidate().call()
    candidate = str(candidate)
    return {"Candidate": candidate}