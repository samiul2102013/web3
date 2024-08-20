from solcx import compile_standard
import json
from web3 import Web3
import os

from dotenv import load_dotenv
load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compilted_code", "w") as file:
    json.dump(compiled_sol, file)

#getting byte code 
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]['object']
#getting abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

#for connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x6BDD17c5559e705a8Db9F1bA98f233e485cE636a"
private_key = os.getenv("PRIVATE_KEY")

#create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode= bytecode)
print(SimpleStorage)

#getting letest transaction 
nonce = w3.eth.get_transaction_count(my_address)
#making a transaction 

transaction = SimpleStorage.constructor().build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# Send it!
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
