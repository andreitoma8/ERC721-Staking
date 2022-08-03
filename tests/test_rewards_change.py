from brownie import NFTCollection, RewardToken, ERC721Staking, accounts, chain

DECIMALS = 10 ** 18
HOUR_IN_SECONDS = 3600
HOURS_TO_PASS = 100
SECONDS_TO_PASS = HOURS_TO_PASS * HOUR_IN_SECONDS
REWARD_PER_HOUR_FOR_ONE_TOKEN = 100000


def test_main():
    # Set up
    owner = accounts[0]
    token = RewardToken.deploy("Rewards Token", "RT", {"from": owner})
    nft = NFTCollection.deploy("NFT Collection", "NFTC", {"from": owner})
    staking = ERC721Staking.deploy(nft.address, token.address, {"from": owner})
    # Mint and Stake NFTs
    for a in range(0, 91):
        accounts.add()
    for i in range(0, 100):
        nft.mint(accounts[i], 1)
        nft.setApprovalForAll(staking.address, True, {"from": accounts[i]})
        nfts = nft.tokensOfOwner(accounts[i].address)
        staking.stake(nfts, {"from": accounts[i]})
    chain.mine(blocks=1, timedelta=3600)
    print(staking.userStakeInfo(owner.address))
    tx = staking.setRewardsPerHour(50000, {"from": owner})
    print(tx.info())
    chain.mine(blocks=1, timedelta=3600)
    print(staking.userStakeInfo(owner.address))
