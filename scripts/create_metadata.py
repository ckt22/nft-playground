from enum import Enum
from importlib.metadata import files
import secrets
from metadata.sample_metadata import metadata_template
from brownie import network
from pathlib import Path
import requests
import json
import os

class Breed(Enum):
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    PSYCHIC = 0
    NORMAL = 1
    FAIRY = 2

class Job(Enum):
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    JOBLESS = 0
    STUDENT = 1
    DEVELOPER = 2


def main():
    for id in range(2,3):
        metadata_file_name = f"./metadata/{network.show_active()}/{id}.json"
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
            upload_to_pinata(metadata_file_name)
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = f"Sad Cat #{id}"
            collectible_metadata["description"] = "Created by Kit"
            image_path = "./img/" + "cat-" + str(id) + ".jpeg"
            image_uri = upload_to_pinata(image_path)
            collectible_metadata["image"] = image_uri
            collectible_metadata["attributes"] = [
                {"trait_type": "job", "value": Job(secrets.randbelow(3)).name},
                {"trait_type": "breed", "value": Breed(secrets.randbelow(3)).name}
            ]
            print(collectible_metadata)
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            upload_to_pinata(metadata_file_name)


def upload_to_ipfs(filepath):
    print("Uploading....")
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001/"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        print(response.content)
        ipfs_hash = response.json()["Hash"]
        # "./img/0-PUG.png" -> "0-PUG.png"
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri

        # Qmee53EAodWYbfEJjfswd2kjhRMkgxsTTwwjfuXqkbNrN9

def upload_to_pinata(filepath):
    PINATA_BASE_URL = "https://api.pinata.cloud/"
    endpoint = "pinning/pinFileToIPFS"
    # Change this filepath
    filename = filepath.split("/")[-1:][0]
    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
    }

    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        print(response.json())
        ipfs_hash = response.json()["IpfsHash"]

        return "https://gateway.pinata.cloud/ipfs/{}".format(ipfs_hash)