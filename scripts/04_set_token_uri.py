from brownie import network, SimpleCollectible
from scripts.helpful_scripts import OPENSEA_URL, get_account_v2

cats_metadata = [
    "https://gateway.pinata.cloud/ipfs/QmVbEVVViVJd2bMe94cw65JCP7HYHFCJxm4jJ4bcVWbWFY", #1
    "https://gateway.pinata.cloud/ipfs/QmfHMWHtiMzQz8W1S6tynSv9y95HsbDsb6rpgCzYD8nCBW", #2
    "https://gateway.pinata.cloud/ipfs/QmUazBCj8XtWnAjxAgPzaUo6VaPXM5VEoRtEJraEKWbM9V", #3
    "https://gateway.pinata.cloud/ipfs/QmPbYZ14NQbtKTRVGPNG6Ad63kmTzdxyfkkFY7ixpxy2TE", #4
    "https://gateway.pinata.cloud/ipfs/QmYDoS9RXvBb144k9o4gTu3gmPYZr6sXxbJvQp9NP7qe7D", #5
    "https://gateway.pinata.cloud/ipfs/QmQncuntzFQRnHNq9G5Ct4jWXoSb1LoCmCV1HFcEGhmhyU", #6
    "https://gateway.pinata.cloud/ipfs/QmSs4oKNzrd3wWjZsn71y8qv3tcZK3DSoBG7kLzjTMmZSc", #7
]

# you can set the token uri of the token after it is minted
# this is the concept of nft blind box
def main():
    print(f"Working on {network.show_active()}")
    simple_collectible = SimpleCollectible[-1]
    number_of_collectibles = 7
    for token_id in range(1, number_of_collectibles + 1):
        print(f"Setting tokenURI of {token_id}")
        set_tokenURI(token_id, simple_collectible, cats_metadata[token_id - 1])
        # if not simple_collectible.tokenURI(token_id).startswith("https://"):


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account_v2()
    tx = nft_contract._setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button")