## Desc
This is a simple (well-deserving 'dummy') blockchain project in python.
A user can, through a simple interface, create or load a wallet, mine blocks and perform transactions.
All is done using SHA256 standard cryptography protocols.
Its pretty neat overall.
The system supports many nodes and chain propagation/validation is implemented.
This is a project I have great interest in further developing and launching as a service.

## Running
Run node.py in your environment. A server is then launched on localhost:5000.
To run multiple nodes, run multiple instances of node.py specifying a port with:

```<python> node.py -p <port>```

Each node's wallet and copy of the blockchain is stored locally, this needs working on.