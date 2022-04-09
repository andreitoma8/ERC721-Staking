from brownie import NFTCollection, RewardToken, ERC721Staking, accounts, config


def main():
    account = accounts.add(config["wallets"]["from_key"])
    token = RewardToken.deploy(
        "RewardsToken", "RT", {"from": account}, publish_source=True
    )
    nft = NFTCollection.deploy(
        "NFTCollection", "NFTC", {"from": account}, publish_source=True
    )
    staking = ERC721Staking.deploy(
        nft.address, token.address, {"from": account}, publish_source=True
    )
