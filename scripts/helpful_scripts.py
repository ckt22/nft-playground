from brownie import (
    accounts,
    config,
    network
)

LOCAL_BLOCKCHAIN_ENVIRONMENTS=["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS=["mainnet-fork-dev"]

OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

def get_account_v2(index=None, id=None):
    if (index):
        return accounts[index]
    if (id):
        return accounts.load(id)
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS 
    or network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])