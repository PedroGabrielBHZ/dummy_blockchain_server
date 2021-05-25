from functools import reduce
import hashlib as hl
from collections import OrderedDict
from hash_util import hash_string_256, hash_block

# The reward we give to miners (for creating a new block)
MINING_REWARD = 10

# Blockchain's initial block
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}

# Blockchain's initialization
blockchain = [genesis_block]
# Unhandled transactions
open_transactions = []
# Blockchain's owner
owner = "Pedro"
# Blockchain's registered participants
participants = {owner}


def valid_proof(transactions, last_hash, proof) -> str:
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:2] == '00'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant: str) -> float:
    """Calculate and return the balance for a participant."""
    # (empty lists are returned if the person was NOT the sender)
    sender_transactions = [[transaction['amount']
                            for transaction in block['transactions']
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
                               for transaction in block['transactions']
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
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }
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
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['previous_hash'],
                           block['proof']):
            print('Proof of work is invalid')
            return False
    return True

##########################################


waiting_for_input = True

while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Print participants')
    print('5: Check transaction validity')
    print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        transaction_data = get_transaction_data()
        recipient, amount = transaction_data
        if add_transaction(recipient, amount=amount):
            print('Transaction added.')
        else:
            print('Transaction failed.')
        print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_chain():
            print('All transactions are valid')
        else:
            print('There are invalid transactions')
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'corrupt_hacker',
                                  'recipient': 'corrupt_receiver',
                                  'amount': 100.0}]
            }
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Input was invalid, please pick a value from the list!')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        break
    print('Balance of {}: {:6.2f}'.format(owner, get_balance(owner)))
else:
    print('User left!')

print('Done!')
