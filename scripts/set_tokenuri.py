from brownie import network, GameSkin
from scripts.helpful_scripts import OPENSEA_URL, get_skin, get_account

skin_metadata_dic = {
    "ETHERNAUT": "https://ipfs.io/ipfs/Qmef4bgDYJdi2pvZ5BmrARosaNaVikEoBN29NVaSjcM43b?filename=4-ETHERNAUT.json",
    "TAGGER": "https://ipfs.io/ipfs/QmbWFkPVpt8e43bdTLQeiuJPs2z2u9Y6bRsDwT9CqDdVn2?filename=2-TAGGER.json",
    "TARS": "https://ipfs.io/ipfs/QmWMXLmNGyknQ559EZ3JSRm1gWGiC6rXahHhfzqAq4yy6i?filename=0-TARS.json",
}


def main():
    print(f"Working on {network.show_active()}")
    game_skin = GameSkin[-1]
    number_of_skins = game_skin.tokenCounter()
    print(f"You have {number_of_skins} tokenIds")
    for token_id in range(number_of_skins):
        skin = get_skin(game_skin.tokenIdToSkin(token_id))
        if not game_skin.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id, game_skin, skin_metadata_dic[skin])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button")
