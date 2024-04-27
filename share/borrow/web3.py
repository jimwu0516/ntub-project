from web3 import Web3, Account
import os, json
from django.conf import settings
from web3.middleware import geth_poa_middleware

rpc_url = 'https://rpc.ankr.com/bsc_testnet_chapel'
web3 = Web3(Web3.HTTPProvider(rpc_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

def load_contract_abi():
    abi_path = os.path.join(settings.STATICFILES_DIRS[0], 'abi', 'ShareTokenABI.json')
    with open(abi_path, 'r') as file:
        contract_abi = json.load(file)
    return contract_abi

contract_address = '0x146dBaE602B862835797c82011cdFe1AbCcb46F0'
abi = load_contract_abi()
contract = web3.eth.contract(address=contract_address, abi=abi)
chainId = '0x61'; #mainnet 0x38 testnet 0x61

owner_private_key = settings.PRIVATE_KEY
owner_account = Account.from_key(owner_private_key)

def send_transaction(contract_function, to_address, *args, **kwargs):
    nonce = web3.eth.get_transaction_count(owner_account.address, 'pending')
    transaction = contract_function(*args).build_transaction({
        'chainId': chainId,
        'gas': 2000000,
        'nonce': nonce,
        **kwargs  
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, owner_private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    

def airdrop_token(to_address, amount):
    
    return send_transaction(contract.functions.airdropTo, to_address, to_address, amount)


def return_deposit(borrower_address, contributor_address, amount, damagePercentage):
    
    return send_transaction(contract.functions.returnDeposit, borrower_address, borrower_address, contributor_address, amount, damagePercentage)
  


