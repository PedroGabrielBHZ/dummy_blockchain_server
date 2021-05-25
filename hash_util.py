import hashlib as hl
import json


def hash_string_256(string):
    return hl.sha256(string).hexdigest()


def hash_block(block: dict) -> str:
    """Hash a blockchain's block and return its representation."""
    # return '-'.join([str(block[key]) for key in block])
    return hl.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
