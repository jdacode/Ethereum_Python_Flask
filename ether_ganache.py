from web3 import Web3
import json

'''In general, an ABI is the interface between two program modules, 
one of which is often at the level of machine code. 
The interface is the de facto method for encoding/decoding 
data into/out of the machine code.

In Ethereum, it's basically how you can encode Solidity contract 
calls for the EVM and, backwards, how to read the data out 
of transactions.
'''

'''
https://remix.ethereum.org/#optimize=false&evmVersion=null&appVersion=0.8.0&version=soljson-v0.4.21+commit.dfe3193c.js
pragma solidity ^0.4.21;

contract Greeter {
    string public greeting;

    function Greeter() public {
        greeting = 'Hello';
    }
    
    function setGreeting(string _greeting) public {
        greeting = _greeting;
    }
    
    function greet() view public returns (string) {
        return greeting;
    }
}
'''



class Ganache:
    def __init__(self):
        self._ganache_url = "HTTP://127.0.0.1:7545"
        self.__web3 = Web3(Web3.HTTPProvider(self._ganache_url))

    def is_connected(self):
        ganache_conn = self.__web3.isConnected()
        ganache_blocks = self.__web3.eth.blockNumber
        return ganache_conn, ganache_blocks

    def ganache_send_amount(self, sender, recipient, key, amount):
        # get the nonce - prevent to send the transaction twice
        nonce = self.__web3.eth.getTransactionCount(sender)
        print("TX= ", nonce)
        # Build the transaction
        tx = {
            'nonce': nonce,  # prevent to send the transaction twice
            'to': recipient,
            'value': self.__web3.toWei(amount, 'ether'),
            'gas': 2000000,  # unit to pay to miners
            'gasPrice': self.__web3.toWei('50', 'gwei')
        }
        print("TX= ", tx)
        # Sign the transaction
        signed_tx = self.__web3.eth.account.signTransaction(tx, key)
        print("SEGNED_TX= ", signed_tx)
        # send the transaction
        tx_hash = self.__web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print("TX_HASH= ", tx_hash)
        print("TX_HASH_toHex= ", self.__web3.toHex(tx_hash))
        # get transaction hash


    def smart_contract_abi_read(self, smartcontract_address):
        self.__web3.eth.defaultAccount = self.__web3.eth.accounts[0]
        abi = json.loads('[{"constant":false,"inputs":[{"name":"_greeting","type":"string"}],"name":"setGreeting","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"greet","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"greeting","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
        address = self.__web3.toChecksumAddress(smartcontract_address)
        contract = self.__web3.eth.contract(address=address, abi=abi)
        return contract.functions.greet().call()

    def smart_contract_abi_write(self, smartcontract_address, data):
        self.__web3.eth.defaultAccount = self.__web3.eth.accounts[0]
        abi = json.loads('[{"constant":false,"inputs":[{"name":"_greeting","type":"string"}],"name":"setGreeting","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"greet","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"greeting","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
        address = self.__web3.toChecksumAddress(smartcontract_address)
        contract = self.__web3.eth.contract(address=address, abi=abi)
        tx_hash = contract.functions.setGreeting(data).transact()
        print('tx_hash= ', tx_hash)
        self.__web3.eth.waitForTransactionReceipt(tx_hash)
        print('UPDATED GREETING= {}'.format(contract.functions.greet().call()))
        return contract.functions.greet().call()


    def smart_contract_abi_read_all(self, smartcontract_address):
        self.__web3.eth.defaultAccount = self.__web3.eth.accounts[0]
        abi = json.loads('[{"constant":false,"inputs":[{"name":"_greeting","type":"string"}],"name":"setGreeting","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"greet","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"greeting","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
        address = self.__web3.toChecksumAddress(smartcontract_address)
        contract = self.__web3.eth.contract(address=address, abi=abi)
        latest = self.__web3.eth.blockNumber
        print("BLOCKS= ", latest)
        print("LATEST BLOCK= ", self.__web3.eth.getBlock(latest))
        list = []
        for i in range(0, latest):
            print("GET BLOCK= ", self.__web3.eth.getBlock(latest - i))
            block = self.__web3.eth.getBlock(latest - i)
            print(block['transactions'])
            print(type(block['transactions']))
            var_hash = self.__web3.toHex(block['transactions'][0])
            print("TYPE HASH= " + str(type(var_hash)))
            print("TX_HASH_toHex= ", var_hash)
            print("HASH= ", self.__web3.eth.getTransactionByBlock(var_hash, 0))
            transaction = self.__web3.eth.getTransaction(var_hash)
            print("TRANSACTIONS= " + str(transaction))
            print(latest)
            print("i= " + str(i))
            print("latest - i= " + str(latest - i))
            print("transaction.input= " + transaction.input)
            tinp = transaction.input
            if ((latest - i) != 1 and (latest - i) != 0) and (tinp != "0x"):
                deco = contract.decode_function_input(tinp)
                print("decode= " + str(deco[1]))
                list.append(" BLOCK(" + str(latest - i) + ")='" + deco[1]['_greeting'] + "' ............. ")
        print(list)
        return list


    def smart_contract_bytecode(self, smartcontract_bytecode):
        print("smartcontract_bytecode= " + smartcontract_bytecode)
        self.__web3.eth.defaultAccount = self.__web3.eth.accounts[0]
        abi = json.loads('[{"constant":false,"inputs":[{"name":"_greeting","type":"string"}],"name":"setGreeting","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"greet","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"greeting","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
        contract = self.__web3.eth.contract(abi=abi, bytecode=smartcontract_bytecode)
        tx_hash = contract.constructor().transact()
        print("tx_hash= ", tx_hash)
        tx_receipt = self.__web3.eth.waitForTransactionReceipt(tx_hash)
        print("tx_receipt= ", tx_receipt)
        real_contract = self.__web3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=abi
        )
        return real_contract.functions.greet().call()