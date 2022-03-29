from brownie import network, accounts, config
from web3 import Web3

LocalBlockchainNetworks = ["development", "GanacheLocal"]


def GetAccount():
    if network.show_active() in LocalBlockchainNetworks:
        return accounts[0]
    else:
        return accounts.add(config["Wallets"]["PrivateKey"])


def PublishSourceDecision():
    if network.show_active() not in LocalBlockchainNetworks:
        return True
    else:
        return False
