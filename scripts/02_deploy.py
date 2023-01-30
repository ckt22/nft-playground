from scripts.helpful_scripts import get_account_v2
from brownie import config, network, SimpleCollectible

def deploy():
    account = get_account_v2()
    simple_collectible = SimpleCollectible.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"]
    )
    print(simple_collectible.address)

def main():
    deploy()
