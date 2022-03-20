from scripts.helpful_scripts import get_account_v2, OPENSEA_URL
from brownie import SimpleCollectible

sample_token_uri = "https://gateway.pinata.cloud/ipfs/Qme4UEoH6NJYyHeFdDHuakjHKPd3Y8SKcjcZnS1xpXMcv8"

def deploy_and_create():
    account = get_account_v2()
    simple_collectible = SimpleCollectible[-1]
    tx = simple_collectible.createCollectible(account.address, sample_token_uri, {"from": account})
    tx.wait(1)
    return simple_collectible

def main():
    deploy_and_create()