from brownie import NFTCollection, RewardToken, ERC721Staking, accounts, chain


def test_main():
    # Set up
    owner = accounts[0]
    token = RewardToken.deploy("Rewards Token", "RT", {"from": owner})
    nft = NFTCollection.deploy("NFT Collection", "NFTC", {"from": owner})
    staking = ERC721Staking.deploy(nft.address, token.address, {"from": owner})
    # Test
    nft.mint(owner.address, 3, {"from": owner})
    for i in range(1, 4):
        nft.approve(staking.address, i, {"from": owner})
    stake_tx_1 = staking.stake([1, 2, 3], {"from": owner})
    withdraw_tx_1 = staking.withdraw([1], {"from": owner})
    withdraw_tx_2 = staking.withdraw([2, 3], {"from": owner})
    assert nft.ownerOf(3) == owner.address
