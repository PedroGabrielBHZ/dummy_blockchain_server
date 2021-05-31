from functools import reduce
import json

from hash_util import hash_block
from block import Block
from transaction import Transaction
from verification import Verification

# The reward we give to miners (for creating a new block)
MINING_REWARD = 10


class Blockchain:
    def __init__(self, hosting_node_id) -> None:
        # Blockchain's initial block
        genesis_block = Block(0, '', [], 100, 0)
        # Initializing empty blockchain list
        self.chain = [genesis_block]
        # Unhandled transactions
        self.open_transactions = []
        self.hosting_node = hosting_node_id
        self.load_data()

    def load_data(self):
        """Initialize blockchain + open transactions data from a file."""
        try:
            with open('blockchain.txt', mode='r') as f:
                file_content = f.readlines()
                blockchain = json.loads(file_content[0][:-1])

                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'],
                                                tx['recipient'],
                                                tx['amount']
                                                ) for tx in block['transactions']]
                    updated_block = Block(block['index'],
                                          block['previous_hash'],
                                          converted_tx,
                                          block['proof'],
                                          block['timestamp']
                                          )
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain

                self.open_transactions = json.loads(file_content[1])
                updated_transactions = []
                for tx in self.open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'], tx['recipient'], tx['amount']
                    )
                    updated_transactions.append(updated_transaction)
                self.open_transactions = updated_transactions
        except (IOError, IndexError):
            pass

    def save_data(self):
        try:
            with open('blockchain.txt', mode='w') as f:
                saveable_chain = [
                    block.__dict__ for block in [
                        Block(block_el.index,
                              block_el.previous_hash,
                              [tx.__dict__ for tx in block_el.transactions],
                              block_el.proof,
                              block_el.timestamp) for block_el in self.chain
                    ]
                ]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.open_transactions]
                f.write(json.dumps(saveable_tx))
        except IOError:
            print('Saving failed!')

    def proof_of_work(self):
        """Generate a proof of work for the open transactions, the hash of the
        previous block and a random number (which is guessed until it fits)."""
        last_block = self.chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        # Try different PoW numbers and return the first valid one
        verifier = Verification()
        while not verifier.valid_proof(self.open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self) -> float:
        """Calculate and return the balance for a participant."""
        participant = self.hosting_node
        # (empty lists are returned if the person was NOT the sender)
        sender_transactions = [[transaction.amount
                                for transaction in block.transactions
                                if transaction.sender == participant]
                               for block in self.chain]

        # (empty lists are returned if the person was NOT the sender)
        sender_open_transactions = [transaction.amount
                                    for transaction in self.open_transactions
                                    if transaction.sender == participant]
        sender_transactions.append(sender_open_transactions)

        amount_sent = reduce(
            (lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
             if len(tx_amt) > 0 else tx_sum + 0),
            sender_transactions, 0
        )

        # We ignore open transactions here because you shouldn't be able to spend
        # coins before the transaction was confirmed + included in a block
        recipient_transactions = [[transaction.amount
                                   for transaction in block.transactions
                                   if transaction.recipient == participant]
                                  for block in self.chain]

        amount_received = reduce(
            (lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
             if len(tx_amt) > 0 else tx_sum + 0),
            recipient_transactions, 0
        )

        return amount_received - amount_sent

    def get_last_blockchain_value(self) -> float:
        """Return the last value of the current blockchain."""
        if len(self.chain) < 1:
            return None
        return self.chain[-1]

    def add_transaction(self, recipient: str, sender: str, amount: float = 1.0):
        """Append new transaction as well as the last blockchain value to the
        blockchain.

        Args:
            sender: The sender of the coins.
            recipient: The recipient of the coins.
            amount: The amount of coins sent with the transaction (default = 1.0)
        """
        transaction = Transaction(sender, recipient, amount)
        verifier = Verification()
        if verifier.verify_transaction(transaction, self.get_balance):
            self.open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self) -> bool:
        """Mine block, return True to clear open transactions list."""
        last_block = self.chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()

        reward_transaction = Transaction(
            'MINING', self.hosting_node, MINING_REWARD)

        # Copy instead of manipulating the original open_transactions list.
        # This ensures that if for some reason the mining should fail, we don't
        # have the reward transaction stored in the open transactions.
        copied_transactions = self.open_transactions[:]
        copied_transactions.append(reward_transaction)
        block = Block(len(self.chain), hashed_block,
                      copied_transactions, proof)
        self.chain.append(block)
        self.open_transactions = []
        self.save_data()
        return True
