from functools import reduce
from collections import OrderedDict
from hash_util import hash_string_256, hash_block
from block import Block
import json
# import pickle

# The reward we give to miners (for creating a new block)
MINING_REWARD = 10
# Blockchain's initialization
blockchain = []
# Unhandled transactions
open_transactions = []
# Blockchain's owner
owner = "Pedro"
# Blockchain's registered participants
participants = {owner}


def load_data():
    global blockchain
    global open_transactions
    try:
        with open('blockchain.txt', mode='r') as f:
            file_content = f.readlines()
            blockchain = json.loads(file_content[0][:-1])
            updated_blockchain = []
            for block in blockchain:
                updated_block = Block(block['index'],
                                      block['previous_hash'],
                                      ([OrderedDict([
                                          ('sender', tx['sender']),
                                          ('recipient', tx['recipient']),
                                          ('amount', tx['amount'])
                                      ]) for tx in block['transactions']]),
                                      block['proof'],
                                      block['timestamp']
                                      )
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain

            open_transactions = json.loads(file_content[1])
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = OrderedDict([
                    ('sender', tx['sender']),
                    ('recipient', tx['recipient']),
                    ('amount', tx['amount'])]
                )
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions

    except IOError:
        # Blockchain's initial block
        genesis_block = Block(0, '', [], 100, 0)
        # Blockchain's initialization
        blockchain = [genesis_block]
        # Unhandled transactions
        open_transactions = []


load_data()


def save_data():
    try:
        with open('blockchain.txt', mode='w') as f:
            f.write(json.dumps(blockchain))
            f.write('\n')
            f.write(json.dumps(open_transactions))

    except IOError:
        print('Saving failed!')


def valid_proof(transactions, last_hash, proof) -> bool:
    """Validate a proof of work number and see if it solves the puzzle
    algorithm (two leading 0s).

    Arguments:
        :transactions: The transactions of the block for which the proof is created.
        :last_hash: The previous block's hash which will be stored in the current block.
        :proof: The proof number we're testing.
    """
    # Create a string with all the hash inputs
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    # print(guess)

    # Hash the string
    # IMPORTANT: This is NOT the same hash as will be stored in the previous_hash.
    # It's not a block's hash. It's only used for the proof-of-work algorithm.
    guess_hash = hash_string_256(guess)
    # print(guess_hash)

    # Only a hash (which is based on the above inputs) which starts with two 0s
    # is treated as valid.
    # This condition is of course defined by you. You could also require 10
    # leading 0s - this would take significantly longer (and this allows you to
    # control the speed at which new blocks can be added)
    return guess_hash[0:2] == '00'


def proof_of_work():
    """Generate a proof of work for the open transactions, the hash of the
    previous block and a random number (which is guessed until it fits)."""
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    # Try different PoW numbers and return the first valid one
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant: str) -> float:
    """Calculate and return the balance for a participant."""
    # (empty lists are returned if the person was NOT the sender)
    sender_transactions = [[transaction['amount']
                            for transaction in block.transactions
                            if transaction['sender'] == participant]
                           for block in blockchain]

    # (empty lists are returned if the person was NOT the sender)
    sender_open_transactions = [transaction['amount']
                                for transaction in open_transactions
                                if transaction['sender'] == participant]
    sender_transactions.append(sender_open_transactions)

    amount_sent = reduce(
        (lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
         if len(tx_amt) > 0 else tx_sum + 0),
        sender_transactions, 0
    )

    # We ignore open transactions here because you shouldn't be able to spend
    # coins before the transaction was confirmed + included in a block
    recipient_transactions = [[transaction['amount']
                               for transaction in block.transactions
                               if transaction['recipient'] == participant]
                              for block in blockchain]

    amount_received = reduce(
        (lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
         if len(tx_amt) > 0 else tx_sum + 0),
        recipient_transactions, 0
    )

    return amount_received - amount_sent


def get_last_blockchain_value() -> float:
    """Return the last value of the current blockchain."""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction: dict) -> bool:
    """Verify if sender has enough balance to send transaction's amount."""
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def add_transaction(recipient: str, sender: str = owner,  amount: float = 1.0):
    """Append new transaction as well as the last blockchain value to the
    blockchain.

    Args:
        sender: The sender of the coins.
        recipient: The recipient of the coins.
        amount: The amount of coins sent with the transaction (default = 1.0)
    """
    transaction = OrderedDict([
        ('sender', sender),
        ('recipient', recipient),
        ('amount', amount)
    ])
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True
    return False


def mine_block() -> bool:
    """Mine block, return True to clear open transactions list."""
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()

    reward_transaction = OrderedDict([
        ('sender', 'MINING'),
        ('recipient', owner),
        ('amount', MINING_REWARD)
    ])

    # Copy instead of manipulating the original open_transactions list.
    # This ensures that if for some reason the mining should fail, we don't
    # have the reward transaction stored in the open transactions.
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    blockchain.append(block)
    return True


def get_transaction_data() -> float:
    """Return the input of the user (a new transaction amount)."""
    transaction_recipient = input('Enter the recipient of the transaction: ')
    transaction_amount = float(input('Your transaction amount, please: '))
    return (transaction_recipient, transaction_amount)


def get_user_choice() -> str:
    """Prompt user for interface choice."""
    user_input = input('Your choice: ')
    return user_input


def print_blockchain_elements():
    """Output blockchain list to the console."""
    for block in blockchain:
        print('Outputting block')
        print(block)
    else:
        print('-' * 20)


def verify_chain() -> bool:
    """Verify blockchain integrity. Return False if it is corrupted."""
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block.previous_hash != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block.transactions[:-1], block.previous_hash,
                           block.proof):
            print('Proof of work is invalid')
            return False
    return True


def verify_transactions() -> bool:
    """Verify all open transactions."""
    return all([verify_transaction(tx) for tx in open_transactions])


###############################################################################
waiting_for_input = True

# A while loop for the user input interface
# It's a loop that exits once waiting_for_input becomes False or when break is called
while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Output participants')
    print('5: Check transaction validity')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_data()
        recipient, amount = tx_data
        # Add the transaction amount to the blockchain
        if add_transaction(recipient, amount=amount):
            print('Added transaction!')
        else:
            print('Transaction failed!')
        print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('There are invalid transactions')
    elif user_choice == 'q':
        # This will lead to the loop to exist because it's running condition becomes False
        waiting_for_input = False
    else:
        print('Input was invalid, please pick a value from the list!')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        # Break out of the loop
        break
    print('Balance of {}: {:6.2f}'.format(owner, get_balance(owner)))
else:
    print('User left!')


print('Done!')
