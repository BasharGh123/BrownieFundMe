from brownie import FundMe, accounts, network, config

LocalBlockchainNetworks = ["development", "GanacheLocal"]
ForkedNetworks = ["mainnet-fork-dev"]


def GetAccount():
    if (
        network.show_active() in LocalBlockchainNetworks
        or network.show_active() in ForkedNetworks
    ):
        return accounts[0]
    else:
        return accounts.add(config["Wallets"]["PrivateKey"])


def Fund():
    FundMeContract = FundMe[-1]
    Account = GetAccount()
    EntranceFee = FundMeContract.GetEntranceFee()
    EntranceFeeInWei = EntranceFee
    EntranceFeeInGwei = EntranceFeeInWei / (10 ** 9)
    EntranceFeeInEth = EntranceFeeInGwei / (10 ** 9)
    EntranceFeeInUsd = FundMeContract.GetConversionRate(EntranceFeeInWei) / (10 ** 27)
    Funding = FundMeContract.FundThisContract(
        {"from": Account, "value": EntranceFeeInWei}
    )
    Funding.wait(1)


def Withdraw():
    FundMeContract = FundMe[-1]
    Account = GetAccount()
    WithdrawAllBalance = FundMeContract.WithdrawAll({"from": Account})
    WithdrawAllBalance.wait(1)


def main():
    FundMeContract = FundMe[-1]

    def ShowBalance():
        return FundMeContract.GetContractBalance()

    print(ShowBalance())

    Fund()

    print(ShowBalance())

    Withdraw()

    print(ShowBalance())
