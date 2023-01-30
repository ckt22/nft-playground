from scripts.helpful_scripts import get_account_v2, OPENSEA_URL
from brownie import SimpleCollectible

cats_metadata = [
    "https://gateway.pinata.cloud/ipfs/QmVbEVVViVJd2bMe94cw65JCP7HYHFCJxm4jJ4bcVWbWFY", #1
    "https://gateway.pinata.cloud/ipfs/QmfHMWHtiMzQz8W1S6tynSv9y95HsbDsb6rpgCzYD8nCBW", #2
    "https://gateway.pinata.cloud/ipfs/QmUazBCj8XtWnAjxAgPzaUo6VaPXM5VEoRtEJraEKWbM9V", #3
    "https://gateway.pinata.cloud/ipfs/QmPbYZ14NQbtKTRVGPNG6Ad63kmTzdxyfkkFY7ixpxy2TE", #4
    "https://gateway.pinata.cloud/ipfs/QmYDoS9RXvBb144k9o4gTu3gmPYZr6sXxbJvQp9NP7qe7D", #5
    "https://gateway.pinata.cloud/ipfs/QmQncuntzFQRnHNq9G5Ct4jWXoSb1LoCmCV1HFcEGhmhyU", #6
    "https://gateway.pinata.cloud/ipfs/QmSs4oKNzrd3wWjZsn71y8qv3tcZK3DSoBG7kLzjTMmZSc", #7
]

def deploy_and_create():
    account = get_account_v2()
    simple_collectible = SimpleCollectible[-1]
    for idx in range(0,8):
        tx = simple_collectible.createCollectible(account.address, cats_metadata[idx], {"from": account})
        tx.wait(1)

def main():
    deploy_and_create()