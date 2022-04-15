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
    # Assert stake
    for i in range(1, 6):
        nft.approve(staking.address, i, {"from": owner})
    stake_tx_1 = staking.stake([1, 2], {"from": owner})
    stake_info_1 = staking.userStakeInfo(owner.address, {"from": owner})
    assert stake_info_1[0] == 2 and stake_info_1[1] >= 0
    # Assert rewards accumulation in time
    chain.mine(blocks=100, timedelta=SECONDS_TO_PASS)
    stake_info_2 = staking.userStakeInfo(owner.address, {"from": owner})
    assert (
        stake_info_2[0] == 2
        and stake_info_2[1]
        >= REWARD_PER_HOUR_FOR_ONE_TOKEN * stake_info_2[0] * HOURS_TO_PASS
    )
    # Assert staking on top of another stake
    stake_tx_1 = staking.stake([3, 4, 5], {"from": owner})
    stake_info_3 = staking.userStakeInfo(owner.address, {"from": owner})
    assert stake_info_3[0] == 5 and stake_info_3[1] == stake_info_2[1]
    # Assert rewards accumulation in time
    chain.mine(blocks=100, timedelta=SECONDS_TO_PASS)
    stake_info_4 = staking.userStakeInfo(owner.address, {"from": owner})
    assert (
        stake_info_4[0] == 5
        and stake_info_4[1]
        >= (REWARD_PER_HOUR_FOR_ONE_TOKEN * stake_info_4[0] * HOURS_TO_PASS)
        + stake_info_2[1]
    )
    # Assert withdraw
    token.transfer(staking.address, 1000000 * DECIMALS, {"from": owner})
    withdraw_tx_1 = staking.withdraw([1, 5], {"from": owner})
    stake_info_5 = staking.userStakeInfo(owner.address, {"from": owner})
    assert stake_info_5[0] == 3 and stake_info_5[1] == stake_info_4[1]
    # Assert rewards accumulation in time after first withdrawal
    chain.mine(blocks=100, timedelta=SECONDS_TO_PASS)
    stake_info_6 = staking.userStakeInfo(owner.address, {"from": owner})
    assert (
        stake_info_6[0] == 3
        and stake_info_6[1]
        >= (REWARD_PER_HOUR_FOR_ONE_TOKEN * stake_info_6[0] * HOURS_TO_PASS)
        + stake_info_5[1]
    )
    # Assert claim rewards
    balance_before_claim = token.balanceOf(owner.address, {"from": owner})
    cliam_rewards_tx = staking.claimRewards({"from": owner})
    balance_after_claim = token.balanceOf(owner.address, {"from": owner})
    assert balance_before_claim == balance_after_claim - stake_info_6[1]
    # Assert available rewards after claim
    stake_info_7 = staking.userStakeInfo(owner.address, {"from": owner})
    assert stake_info_7[1] == 0
