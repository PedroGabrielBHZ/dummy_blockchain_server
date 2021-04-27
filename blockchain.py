# Initializing our (empty) blockchain list
blockchain = []
open_transactions = []
owner = "Pedro"


def get_last_blockchain_value() -> float:
    """Return the last value of the current blockchain."""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(sender: str, recipient: str, amount: float = 1.0):
    """Append a new transaction as well as the last blockchain value to the
    blockchain.

    Args:
        sender: The sender of the coins.
        recipient: The recipient of the coins.
        amount: The amount of coins sent with the transaction (default = 1.0)
    """
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    open_transactions.append(transaction)


def mine_block():
    pass


def get_transaction_data() -> float:
    """Return the input of the user (a new transaction amount)."""
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your transaction amount, please: '))
    return (tx_recipient, tx_amount)


def get_user_choice() -> str:
    """Prompt user for interface choice."""
    user_input = input('Your choice: ')
    return user_input


def print_blockchain_elements():
    """Output the blockchain list to the console."""
    for block in blockchain:
        print('Outputting block')
        print(block)
    else:
        print('-' * 20)


def verify_chain() -> bool:
    """Verify blockchain integrity."""
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
    return is_valid


waiting_for_input = True

while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Output the blockchain blocks')
    print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_data()
        add_transaction(, get_last_blockchain_value())
    elif user_choice == '2':
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Input was invalid, please pick a value from the list!')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        break
else:
    print('User left!')


print('Done!')
