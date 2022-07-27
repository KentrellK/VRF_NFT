from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
    get_account,
)
from brownie import network, GameSkin
import pytest
from scripts.deploy_and_create import deploy_and_create


def test_can_create_skin():
    # deploy the contract
    # Create an NFT
    # get a random skin back
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Act
    game_skin, creation_transaction = deploy_and_create()
    requestId = creation_transaction.events["requestedSkin"]["requestId"]
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, game_skin.address, {"from": get_account()}
    )
    # Assert
    assert game_skin.tokenCounter() == 1
    # 777 % 3 = 0 so our skin should be 0 aka Ethernaut
    assert game_skin.tokenIdToSkin(0) == random_number % 3
