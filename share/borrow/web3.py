from web3 import Web3, Account
import os, json
from django.conf import settings
from web3.middleware import geth_poa_middleware
import requests
from users.models import Profile

rpc_url = 'https://data-seed-prebsc-1-s2.bnbchain.org:8545'
web3 = Web3(Web3.HTTPProvider(rpc_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

def load_contract_abi():
    
    abi_path = os.path.join(settings.STATICFILES_DIRS[0], 'abi', 'ShareTokenABI.json')
    with open(abi_path, 'r') as file:
        contract_abi = json.load(file)
    return contract_abi

contract_address = '0xFa0D29E5ab2B9082B1E56734574d307a69AC08BC'
chain_id = '0x61'; #mainnet 0x38 testnet 0x61
abi = load_contract_abi()
contract = web3.eth.contract(address=contract_address, abi=abi)

owner_private_key = os.getenv('PRIVATE_KEY')
if not owner_private_key:
    raise ValueError("PRIVATE_KEY environment variable is not set")

owner_account = Account.from_key(owner_private_key)



def returnDepositAndAirdrop(borrower_address, contributor_address, depositAmount, damagePercentage, airdropAmount):
    nonce = web3.eth.get_transaction_count(owner_account.address)
    transaction = contract.functions.returnDepositAndAirdrop(borrower_address, contributor_address, depositAmount, damagePercentage, airdropAmount).build_transaction({
        'chainId': chain_id, 
        'gas': 2000000,
        'nonce': nonce,
    })
    
    signed_txn = web3.eth.account.sign_transaction(transaction, owner_private_key)
    signed_txn_raw = signed_txn.rawTransaction
    txn_hashtxn_hash = web3.eth.send_raw_transaction(signed_txn_raw)
    
    return txn_hashtxn_hash.hex()
    
def borrowerNotPickedUpReturnDeposit(borrower_address, contributor_address, depositAmount) :
    nonce = web3.eth.get_transaction_count(owner_account.address)
    transaction = contract.functions.borrowerNotPickedUpReturnDeposit(borrower_address, contributor_address, depositAmount).build_transaction({
        'chainId': chain_id,  
        'gas': 2000000,
        'nonce': nonce,
    })
    
    signed_txn = web3.eth.account.sign_transaction(transaction, owner_private_key)
    signed_txn_raw = signed_txn.rawTransaction
    txn_hashtxn_hash = web3.eth.send_raw_transaction(signed_txn_raw)
    
def cancelOrderReturnDeposit(borrower_address, depositAmount) :
    nonce = web3.eth.get_transaction_count(owner_account.address)
    transaction = contract.functions.cancelOrderReturnDeposit(borrower_address, depositAmount).build_transaction({
        'chainId': chain_id, 
        'gas': 2000000,
        'nonce': nonce,
    })
    
    signed_txn = web3.eth.account.sign_transaction(transaction, owner_private_key)
    signed_txn_raw = signed_txn.rawTransaction
    txn_hashtxn_hash = web3.eth.send_raw_transaction(signed_txn_raw)

def get_next_unlock():
    result = contract.functions.nextUnlock().call()
    return {'days': result[0], 'hours': result[1]}

def unlock_tokens():
    nonce = web3.eth.get_transaction_count(owner_account.address)
    transaction = contract.functions.unlockTokens().build_transaction({
        'chainId': int(chain_id, 16), 
        'gas': 2000000,
        'nonce': nonce,
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, owner_private_key)
    signed_txn_raw = signed_txn.rawTransaction
    txn_hashtxn_hash = web3.eth.send_raw_transaction(signed_txn_raw)
    return txn_hashtxn_hash.hex()

def get_airdrop_mint():
    airdrop_mint = contract.functions.airdropMint().call()
    return airdrop_mint

def get_top_token_holders():
    profiles = Profile.objects.all()

    balances = {}

    for profile in profiles:
        address = profile.airdrop_wallet_address

        if Web3.is_address(address):
            balance = contract.functions.balanceOf(address).call() / 10**18
            balances[address] = balance
        else:
            print(f"Invalid address found: {address}")
            continue

    sorted_balances = sorted(balances.items(), key=lambda item: item[1], reverse=True)

    top_token_holders = sorted_balances[:5]
    
    return top_token_holders

def get_list_end_proposals():
    
    result = contract.functions.listEndProposals().call()
    ids, titles, descriptions, totalYess, totalNos = result
    proposals = []
    for i in range(len(ids)):
        proposals.append({
            'id': ids[i],
            'title': titles[i],
            'description': descriptions[i],
            'totalYes': totalYess[i],
            'totalNo': totalNos[i]
        })
    return proposals

def get_list_active_proposals():
    
    result = contract.functions.listActiveProposals().call()
    ids, titles, descriptions, totalYess, totalNos, remainingMinutes = result
    proposals = []
    for i in range(len(ids)):
        proposals.append({
            'id': ids[i],
            'title': titles[i],
            'description': descriptions[i],
            'totalYes': totalYess[i],
            'totalNo': totalNos[i],
            'remainingMinutes': remainingMinutes[i]
        })
    return proposals    

def get_proposal_info(proposal_id):
    proposal_id = int(proposal_id)
    title, description, totalYes, totalNo =contract.functions.getProposal(proposal_id).call()
    data = {
        'title':title, 
        'description':description, 
        'totalYes':totalYes,
        'totalNo':totalNo,
    }
    return data
    

def get_proposal_details(proposal_id):
    proposal_id = int(proposal_id)
    voters, voting_powers, votes = contract.functions.getVotersDetails(proposal_id).call()

    data = {
        "proposal_id": proposal_id,
        "voters": list(zip(voters, voting_powers, votes)),
    }
    return data


