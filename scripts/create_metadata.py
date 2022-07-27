from brownie import GameSkin, network
from scripts.helpful_scripts import get_skin
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json
import os

skin_to_image_uri = {
    "ETHERNAUT": "https://ipfs.io/ipfs/QmfMJGScdLHWYZ1HY1JJybzsWfMUZqS7R3eYNB3HPExvvB?filename=ethernaut.png",
    "TAGGER": "https://ipfs.io/ipfs/QmfUFyBBTmKi8TMTRA9JLCFwwQJV47GeJfe1DBtX8eNsXx?filename=tagger.png",
    "TARS": "https://ipfs.io/ipfs/QmSNx8aMfFU7Zd2J9TLFvoRhcC9zR6e11Xqi75ZwvfJqpf?filename=tars.png",
}


def main():
    game_skin = GameSkin[-1]
    number_of_skins = game_skin.tokenCounter()
    print(f"You have created {number_of_skins} skins.")
    for token_id in range(number_of_skins):
        skin = get_skin(game_skin.tokenIdToSkin(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{skin}.json"
        )
        skin_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            skin_metadata["name"] = skin
            skin_metadata["description"] = f"A wearable in-game {skin} skin!"
            image_path = "./img/" + skin.lower().replace("_", "-") + ".png"

            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)
            image_uri = image_uri if image_uri else skin_to_image_uri[skin]

            skin_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(skin_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        # "./img/0-ETHERNAUT.png" -> "0-ETHERNAUT.png"
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
