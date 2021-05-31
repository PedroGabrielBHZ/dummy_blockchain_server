from uuid import uuid4
from blockchain import Blockchain
from verification import Verification


class Node:
    def __init__(self) -> None:
        # self.id = str(uuid4())
        self.id = 'Pepe'
        self.blockchain = Blockchain(self.id)

    def get_transaction_data(self) -> float:
        """Return the input of the user (a new transaction amount)."""
        transaction_recipient = input(
            'Enter the recipient of the transaction: ')
        transaction_amount = float(input('Your transaction amount, please: '))
        return (transaction_recipient, transaction_amount)

    def get_user_choice(self) -> str:
        """Prompt user for interface choice."""
        user_input = input('Your choice: ')
        return user_input

    def print_blockchain_elements(self):
        """Output blockchain list to the console."""
        for block in self.blockchain.chain:
            print('Outputting block')
            print(block)
        else:
            print('-' * 20)

    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print('Please choose')
            print('1: Add a new transaction value')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks')
            print('4: Check transaction validity')
            print('q: Quit')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_data()
                recipient, amount = tx_data
                # Add the transaction amount to the blockchain
                if self.blockchain.add_transaction(recipient,
                                                   self.id,
                                                   amount=amount):
                    print('Added transaction!')
                else:
                    print('Transaction failed!')
                print(self.blockchain.open_transactions)
            elif user_choice == '2':
                self.blockchain.mine_block()
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                verifier = Verification()
                if verifier.verify_transactions(
                        self.blockchain.open_transactions,
                        self.blockchain.get_balance):
                    print('All transactions are valid')
                else:
                    print('There are invalid transactions')
            elif user_choice == 'q':
                # This will lead to the loop to exist because it's running
                # condition becomes False
                waiting_for_input = False
            else:
                print('Input was invalid, please pick a value from the list!')
            verifier = Verification()
            if not verifier.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print('Invalid blockchain!')
                # Break out of the loop
                break
            print('Balance of {}: {:6.2f}'.format(
                self.id, self.blockchain.get_balance()))

        else:
            print('User left!')

        print('Done!')

if __name__ == "__main__":
    node = Node()
    node.listen_for_input()