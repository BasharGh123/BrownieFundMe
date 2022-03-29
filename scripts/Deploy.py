from brownie import FundMe, MockV3Aggregator, network, config, accounts

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


def PublishSourceDecision():
    return config["networks"][network.show_active()].get("verify")


def DeployMocks():
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(8, 200000000000, {"from": GetAccount()})


def GetCurrencyPairPriceFeedAddress(CurrencyPair):
    if network.show_active() not in LocalBlockchainNetworks:
        PriceFeedAddress = config["networks"][network.show_active()][CurrencyPair]
        return PriceFeedAddress
    else:
        DeployMocks()
        PriceFeedAddress = MockV3Aggregator[-1].address
        return PriceFeedAddress


def DeployFundMe():
    Account = GetAccount()
    FundMeContract = FundMe.deploy(
        GetCurrencyPairPriceFeedAddress("ETH / USD"),
        {"from": Account},
        publish_source=PublishSourceDecision(),
    )

    AccountBalance = Account.balance()
    AccountBalanceInWei = AccountBalance
    AccountBalanceInGwei = AccountBalance / 10 ** 9
    AccountBalanceInEth = AccountBalance / 10 ** 18
    AccountBalanceInUSD = (
        FundMeContract.GetConversionRate(AccountBalanceInWei) / 10 ** 27
    )

    print(str(AccountBalanceInWei) + " WEI")
    print(str(AccountBalanceInGwei) + " GWEI")
    print(str(AccountBalanceInEth) + " ETH")
    print(str(AccountBalanceInUSD) + " USD")


def main():
    DeployFundMe()
