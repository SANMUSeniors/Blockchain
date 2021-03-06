import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from flask import Flask
from flask import Flask, jsonify, request
class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
    def new_block(self,proot,previous_hash=None):
         """
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block"""
        block ={
            'index':len(self.chain)+1,
            'timestamp':time(),
            'transactions':self.current_transactions,
            'proof':proof,
            'previous_hash':previous_hash or self.hash(self.chain[-1]),
        }
     # Creates a new Block and adds it to the chain
     # Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block
    
    
    def new_transaction(self,sender,recipient,amount):
        """
        
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender':sender,
            'recipient':recipient,
            'amount':amount,
        })
        return self.last_block['index']+1
        # Adds a new transaction to the list of transactions
        pass
    @staticmethod
    def hash(block):
       """
        
        :param block: <dict> Block
        :return: <str>
        """
        block_string = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()  
    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]
    def proof_of_work(self,last_proof):
         """
        
        :param last_proof: <int>
        :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof,proof) is False:
            proof +=1
        return proof
    @staticmethod
    def valid_proof(last_proof,proof):
        """
       
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] =="0000"
# Instantiate our Node
app = Flask(__name__)
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-'��'')
# Instantiate the Blockchain
blockchain = Blockchain()
@app.route('/mine',methods=['GET'])
def mine():
    return "We'll mine a new Block"
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

   
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    block = blockchain.new_block(proof)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200
@app.route('/transactions/new',methods=['Post'])
def new_transaction():
    return "We'll add a new transaction"
    values = request.get_json()
    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201
@app.route('/chain',methods=['GET'])
def full_chain():
    response = {
        'chain':blockchain.chain,
        'length':len(blockchain.chain),
    }
    return jsonify(response),200
if __name__ =='__mian__':
    app.run(host='0.0.0.0',port=5000)


            
        