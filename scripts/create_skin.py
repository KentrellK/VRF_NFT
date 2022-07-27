from brownie import GameSkin
from scripts.helpful_scripts import fund_with_link, get_account
from web3 import Web3


def main():
    account = get_account()
    game_skin = GameSkin[-1]
    fund_with_link(game_skin.address, amount=Web3.toWei(0.1, "ether"))
    creation_transaction = game_skin.createSkin({"from": account})
    creation_transaction.wait(1)
    print("Skin created!")
