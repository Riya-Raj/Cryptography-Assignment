import time
import hashlib
import json
from DES_encryption import *
from random import randint
from os import path

class Block(object):
    difficulty = 3

    def __init__(self, transactions, prevHash, t = None, hash = None, key = None):
        self.data = transactions
        self.time = t or time.asctime()
        self.previousHash = prevHash
        self.key = key or 0

        self.hash = hash or self.calculateHash()

    def calculateHash(self):
        string_block = str(self.previousHash) + str(self.time) + str(self.key) + str(self.data)
        encoded_block = string_block.encode()
        claculateHash = hashlib.sha256(encoded_block)
        hex_hash = claculateHash.hexdigest()
        # des_hash = des256(hex_hash)
        return str(hex_hash)

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

    def json_block(self):
        block = {
            'data' : self.data,
            'previousHash' : self.previousHash,
            'timeStamp' : self.time,
            'hash' : self.hash,
            'key' : self.key
        }
        return block

p = 11
g = 2
verify = 5

class Wallet(object):
    def __init__(self, name, balance, ID = None, th = None):
        self.name = name
        self.balance = balance
        self.userID = ID or randint(0, 10)
        self.transactionHistory = th or []
        self.y = (g**self.userID) % p

    def viewUser(self):
        print("User details and transactions: ")
        print("Wallet: ", self.name)
        print("Balance: ", self.balance)
        print("Transaction Hystory:")
        for t in self.transactionHistory:
            print(t)
        return

    def json_wallet(self):
        wallet = {
            'name' : self.name,
            'balance' : self.balance,
            'ID' : self.userID,
            'th' : self.transactionHistory
        }
        return wallet

    #sender proover
    def geth(self):
        self.r = randint(0, p-1)
        h = (g**self.r) % p
        # print("r : ", self.r)
        # print("h : ", h)
        return h
    def gets(self, b):
        s = (self.r + (b*self.userID)) % (p-1)
        # print("s : ", s)
        return s
    #recipient checker
    def cy(self, y):
        self.cy = y
    def ch(self, h):
        self.ch = h
        self.rb = randint(0, 1)
        # print("b : ", self.rb)
        return self.rb
    def verify(self, s):
        left = (g**s) % p
        right = (self.ch*(self.cy**self.rb)) % p
        # print(left, " ? ", right)
        return left == right
    
class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.wallets = {}

        if(path.exists('BlockChain.json')):
            with open('BlockChain.json', 'r') as bc:
                b = bc.read()
                blocks = json.loads(b)
                for key in blocks:
                    block_loop = Block(blocks[key]["data"], blocks[key]["previousHash"], blocks[key]["timeStamp"], blocks[key]["hash"], blocks[key]["key"])
                    self.chain.append(block_loop)
        else:
            block_start = Block("Genesis Block", "0")
            block_start.mineBlock()
            self.chain.append(block_start)

        if path.exists("Wallets.json"):
            with open('Wallets.json', 'r') as wl:
                w = wl.read()
                wallets = json.loads(w)
                for key in wallets:
                    self.new_wallet(wallets[key]["name"], wallets[key]["balance"], wallets[key]["ID"], wallets[key]["th"])

    def new_wallet(self, wname, balance, ID = None, th = None):
        user = Wallet(wname, balance, ID, th)
        self.wallets[wname] = user

    def make_transaction(self, fromwallet, amount, towallet):
        if self.verifyTransaction(fromwallet, towallet):
            self.wallets[fromwallet].balance -= amount
            self.wallets[fromwallet].transactionHistory.append(str(amount) + " sent to " + str(towallet))
            self.wallets[towallet].balance += amount
            self.wallets[towallet].transactionHistory.append(str(amount) + " recieved from " + str(fromwallet))
            print("Transaction Succeded")
            self.add_transaction(fromwallet, amount, towallet)
        else:
            print("Transaction failed...")

    def verifyTransaction(self, fromwallet, towallet):
        y = self.wallets[fromwallet].y
        # print("y = ", y)
        self.wallets[towallet].cy(y)

        for i in range(0, verify):
            b = self.wallets[towallet].ch(self.wallets[fromwallet].geth())
            return self.wallets[towallet].verify(self.wallets[fromwallet].gets(b))
        
    def createBlock(self):
        t = self.get_transactions()
        self.pending_transactions = []
        ph = self.chain[len(self.chain)-1].hash
        block = Block(t, ph)
        print("Mining...")
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

    def save_chain(self):
        s = {}
        index = 0
        for b in self.chain:
            i = str(index)
            s[i] = b.json_block()
            index += 1
        with open('BlockChain.json', 'w') as bc:
            json.dump(s, bc, indent=4)

    def save_wallets(self):
        s = {}
        for key in self.wallets:
            s[key] = self.wallets[key].json_wallet()
        with open('Wallets.json', 'w') as wl:
            json.dump(s, wl, indent=4)

    def print_chain(self):
        for i in range(0, len(self.chain)):
            print(self.chain[i].print_block())
    

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

    print("Add Wallet : 1")
    print("Make a Transaction : 2")
    print("viewUser : 3")
    print("viewChain : 4")
    print("mine Block : 5")
    print("Quit : 6")
    print("")

    while(1):
        command = input("Enter Command: ")
        command = int(command)
        nTransactions = 0

        if command == 1:
            name = input("Account name: ")
            bal = input("Deposit amount: ")
            BITScoin.new_wallet(str(name), int(bal))

        elif command == 2:
            sender = input("Sender: ")
            recipient = input("Recipient: ")
            amount = input("Amount to transfer: ")
            BITScoin.make_transaction(str(sender), int(amount), str(recipient))
            nTransactions += 1
            if(nTransactions >= 5):
                BITScoin.createBlock()

        elif command == 3:
            user = input("User name: ")
            BITScoin.wallets[str(user)].viewUser()

        elif command == 4:
            BITScoin.print_chain()

        elif command == 5:
            BITScoin.createBlock()
            BITScoin.save_chain()
            BITScoin.save_wallets()

        elif command == 6:
            BITScoin.createBlock()
            BITScoin.save_chain()
            BITScoin.save_wallets()
            break

        print("")
    # BITScoin.new_wallet("Jai", 1000)
    # BITScoin.new_wallet("Red", 500)

    # BITScoin.make_transaction("Jai", 100, "Red")
    # BITScoin.make_transaction("Red", 1000, "Jai")

    # BITScoin.createBlock()

    # print(BITScoin.chain[0].print_block())
    # print(BITScoin.chain[1].print_block())
    # print(isChainValid(BITScoin.chain))

    # BITScoin.print_chain()

    # print(BITScoin.wallets["Jai"].viewUser())

    # BITScoin.save_chain()
    # BITScoin.save_wallets()
