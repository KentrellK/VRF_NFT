from scripts.helpful_scripts import (
    fund_with_link,
    get_account,
    OPENSEA_URL,
    get_contract,
)
from brownie import GameSkin, network, config


def deploy_and_create():
    account = get_account()
    game_skin = GameSkin.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
    )
    fund_with_link(game_skin.address)
    creating_tx = game_skin.createSkin({"from": account})
    creating_tx.wait(1)
    print("New token has been created!")
    return game_skin, creating_tx


def main():
    deploy_and_create()
