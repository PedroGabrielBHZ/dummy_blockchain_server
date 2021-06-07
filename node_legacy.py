from uuid import uuid4
from blockchain import Blockchain
from utility.verification import Verification
from wallet import Wallet


class Node:
    def __init__(self) -> None:
        # self.wallet.public_key = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

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
            print('5: Create wallet')
            print('6: Load wallet')
            print('7: Save keys')
            print('q: Quit')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_data()
                recipient, amount = tx_data
                signature = self.wallet.sign_transaction(self.wallet.public_key,
                                                         recipient, amount)
                if self.blockchain.add_transaction(recipient,
                                                   self.wallet.public_key,
                                                   signature,
                                                   amount=amount):
                    print('Added transaction!')
                else:
                    print('Transaction failed!')
                print(self.blockchain.get_open_transactions())

            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print('Mining failed. Got no wallet?')

            elif user_choice == '3':
                self.print_blockchain_elements()

            elif user_choice == '4':
                if Verification.verify_transactions(
                        self.blockchain.get_open_transactions(),
                        self.blockchain.get_balance):
                    print(5*'\n')
                    print('All transactions are valid')
                    print(5*'\n')
                else:
                    print(5*'\n')
                    print('There are invalid transactions')
                    print(5*'\n')

            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)

            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)

            elif user_choice == '7':
                self.wallet.save_keys()

            elif user_choice == 'q':
                waiting_for_input = False

            else:
                print('Input was invalid, please pick a value from the list!')

            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print('Invalid blockchain!')
                break
            print('Balance of {}: {:6.2f}'.format(
                self.wallet.public_key, self.blockchain.get_balance()))
        else:
            print('User left!')
        print('Done!')


if __name__ == "__main__":
    node = Node()
    node.listen_for_input()
