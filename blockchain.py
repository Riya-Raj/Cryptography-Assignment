import time
import hashlib
import json
from DES_encryption import *
from random import randint

class Block(object):
    difficulty = 3

    def __init__(self, transactions, prevHash):
        self.data = transactions
        self.time = time.asctime()
        self.previousHash = prevHash
        self.key = 0

        self.hash = self.calculateHash()

    def calculateHash(self):
        string_block = str(self.previousHash) + str(self.time) + str(self.key) + str(self.data)
        encoded_block = string_block.encode()
        claculateHash = hashlib.sha256(encoded_block)
        hex_hash = claculateHash.hexdigest()
        des_hash = des256(hex_hash)
        return str(des_hash)

    def mineBlock(self):
        while(self.hash[0:self.difficulty] != self.get_target()):
            self.key = self.key + 1
            self.hash = self.calculateHash()

    def get_target(self):
        target = "0" * self.difficulty
        return target

    def print_block(self):
        print("Transaction: ", self.data)
        print("Time: ", self.time)
        print("Previous Hash: ", self.previousHash)
        print("Self Hash:     ", self.hash)
        print("Proof: ", self.key)
        return ""

    # def json_block(self):


class Wallet(object):
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.userID = randint(0, 10)
        self.transactionHistory = []

    def viewUser(self):
        print("User details and transactions: ")
        print("Wallet: ", self.name)
        print("Balance: ", self.balance)
        print("Transaction Hystory:")
        for t in self.transactionHistory:
            print(t)

class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.wallets = {}

        block_start = Block("Genesis Block", "0")
        block_start.mineBlock()
        self.chain.append(block_start)

    def new_wallet(self, wname, balance):
        user = Wallet(wname, balance)
        self.wallets[wname] = user

    def make_transaction(self, fromwallet, amount, towallet):
        # zkp()

        self.wallets[fromwallet].balance -= amount
        self.wallets[fromwallet].transactionHistory.append(str(amount) + " sent to " + str(towallet))
        self.wallets[towallet].balance += amount
        self.wallets[towallet].transactionHistory.append(str(amount) + " recieved from " + str(fromwallet))

        self.add_transaction(fromwallet, amount, towallet)

    def createBlock(self):
        t = self.get_transactions()
        self.pending_transactions = []
        ph = self.chain[len(self.chain)-1].hash
        block = Block(t, ph)
        print("Mining ", len(self.chain)-1, "block")
        block.mineBlock()
        self.chain.append(block)

    def add_transaction(self, sender, amount, recipient):
        trans = str(sender) + " sent " + str(amount) + " to " + str(recipient) + ". "
        self.pending_transactions.append(trans)
    
    def get_transactions(self):
        transactions = ""
        for s in self.pending_transactions:
            transactions += s
        return transactions

    # def save_chain(self):


def isChainValid(chain):
    for i in range(1, len(chain)):
        cBlock = chain[i]
        pBlock = chain[i-1]
        if(cBlock.hash != cBlock.calculateHash()):
            print("Current Hash is nat equal")
            return False
        if(pBlock.hash != cBlock.previousHash):
            print("Previous Hashes are not equal")
            return False
        if(cBlock.hash[:cBlock.difficulty] != cBlock.get_target()):
            print("This Block has not been mined: ", i)
            return False
    return True



if __name__ == "__main__":
    BITScoin = BlockChain()
    BITScoin.new_wallet("Jai", 1000)
    BITScoin.new_wallet("Red", 500)
    BITScoin.make_transaction("Jai", 100, "Red")

    BITScoin.createBlock()

    print(BITScoin.chain[0].print_block())
    print(BITScoin.chain[1].print_block())
    print(isChainValid(BITScoin.chain))

    print(BITScoin.wallets["Jai"].viewUser())
