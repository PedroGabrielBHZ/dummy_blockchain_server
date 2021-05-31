from hash_util import hash_string_256, hash_block


class Verification:

    def valid_proof(self, transactions, last_hash, proof) -> bool:
        """Validate a proof of work number and see if it solves the puzzle
        algorithm (two leading 0s).

        Arguments:
            :transactions: The transactions of the block for which the proof is created.
            :last_hash: The previous block's hash which will be stored in the current block.
            :proof: The proof number we're testing.
        """
        # Create a string with all the hash inputs
        guess = (str([tx.to_ordered_dict() for tx in transactions]) +
                 str(last_hash) + str(proof)).encode()
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

    def verify_chain(self, blockchain) -> bool:
        """Verify blockchain integrity. Return False if it is corrupted."""
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not self.valid_proof(block.transactions[:-1], block.previous_hash,
                                    block.proof):
                print('Proof of work is invalid')
                return False
            return True

    def verify_transaction(self, transaction: dict, get_balance) -> bool:
        """Verify if sender has enough balance to send transaction's amount."""
        sender_balance = get_balance()
        return sender_balance >= transaction.amount

    def verify_transactions(self, open_transactions: list) -> bool:
        """Verify all open transactions."""
        return all([self.verify_transaction(tx, get_balance)
                    for tx in open_transactions
                    ])