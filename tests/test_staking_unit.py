from brownie import NFTCollection, RewardToken, ERC721Staking, accounts, chain

DECIMALS = 10 ** 18
HOUR_IN_SECONDS = 3600
HOURS_TO_PASS = 100
SECONDS_TO_PASS = HOURS_TO_PASS * HOUR_IN_SECONDS
REWARD_PER_HOUR_FOR_ONE_TOKEN = 100000

def deploy_contracts(deployer):
    reward_token = RewardToken.deploy("Reward Token", "RWT", {"from": deployer})
    nft_collection = NFTCollection.deploy("NFT Collection", "NFT", {"from": deployer})
    staking = ERC721Staking.deploy(nft_collection, reward_token, {"from": deployer})
    return reward_token, nft_collection, staking

def mint_and_approve_nft(to, amount, nft_collection, staking):
    nft_collection.mint(to, amount, {"from": to})
    nft_collection.setApprovalForAll(staking, True, {"from": to})

def test_constructor():
    owner = accounts[0]

    reward_token, nft_collection, staking = deploy_contracts(owner)

    assert staking.rewardsToken() == reward_token.address
    assert staking.nftCollection() == nft_collection.address

def test_stake():
    owner = accounts[0]

    reward_token, nft_collection, staking = deploy_contracts(owner)

    mint_and_approve_nft(owner, 2, nft_collection, staking)
    token_holdings = nft_collection.tokensOfOwner(owner)

    staking.stake(token_holdings, {"from": owner})

    owner_stake_info = staking.userStakeInfo(owner)
    assert owner_stake_info[0] == token_holdings
    assert owner_stake_info[1] == 0
    assert staking.stakersArray(0) == owner

    owner_staker_struct = staking.stakers(owner.address)
    assert owner_staker_struct[0] == chain.time()
    assert owner_staker_struct[1] == 0

    for token_id in token_holdings:
        assert staking.stakerAddress(token_id) == owner
        assert nft_collection.ownerOf(token_id) == staking.address
    

def test_rewards_accumulation():
    owner = accounts[0]

    reward_token, nft_collection, staking = deploy_contracts(owner)

    mint_and_approve_nft(owner, 2, nft_collection, staking)
    token_holdings = nft_collection.tokensOfOwner(owner)

    staking.stake(token_holdings, {"from": owner})

    chain.mine(blocks=10, timedelta=SECONDS_TO_PASS)

    owner_stake_info = staking.userStakeInfo(owner)
    assert owner_stake_info[1] == REWARD_PER_HOUR_FOR_ONE_TOKEN * HOURS_TO_PASS * 2

def test_multiple_staking_tx():
    owner = accounts[0]

    reward_token, nft_collection, staking = deploy_contracts(owner)

    mint_and_approve_nft(owner, 3, nft_collection, staking)
    token_holdings_0 = nft_collection.tokensOfOwner(owner)

    tx_0 = staking.stake(token_holdings_0[:1], {"from": owner})

    chain.mine(blocks=10, timedelta=SECONDS_TO_PASS)

    [tokens_staked_0, available_rewards_0] = staking.userStakeInfo(owner)
    assert tokens_staked_0 == token_holdings_0[:1]
    assert available_rewards_0 == (chain.time() - staking.stakers(owner.address)[0]) * REWARD_PER_HOUR_FOR_ONE_TOKEN * len(tokens_staked_0) / HOUR_IN_SECONDS

    token_holdings_1 = nft_collection.tokensOfOwner(owner)
    
    tx_1 = staking.stake(token_holdings_1, {"from": owner})

    chain.mine(blocks=10, timedelta=SECONDS_TO_PASS)

    [tokens_staked_1, available_rewards_1] = staking.userStakeInfo(owner)
    # assert available_rewards_1 == (chain.time() - staking.stakers(owner.address)[0]) * REWARD_PER_HOUR_FOR_ONE_TOKEN * len(tokens_staked_1) / HOUR_IN_SECONDS + available_rewards_0
    assert tokens_staked_1 == tokens_staked_0 + token_holdings_1

def test_withdraw():
    owner = accounts[0]

    reward_token, nft_collection, staking = deploy_contracts(owner)

    mint_and_approve_nft(owner, 3, nft_collection, staking)
    token_holdings = nft_collection.tokensOfOwner(owner)

    staking.stake(token_holdings, {"from": owner})

    chain.mine(blocks=10, timedelta=SECONDS_TO_PASS)

    staking.withdraw(token_holdings, {"from": owner})

    for token_id in token_holdings:
        assert staking.stakerAddress(token_id) == "0x0000000000000000000000000000000000000000"
        assert nft_collection.ownerOf(token_id) == owner

def test_withdraw_rewards():
    owner = accounts[0]

    reward_token, nft_collection, staking = deploy_contracts(owner)

    mint_and_approve_nft(owner, 3, nft_collection, staking)
    token_holdings = nft_collection.tokensOfOwner(owner)

    staking.stake(token_holdings, {"from": owner})

    chain.mine(blocks=10, timedelta=SECONDS_TO_PASS)

    reward_token.mint(staking.address, 100 * DECIMALS, {"from": owner})

    staking.claimRewards({"from": owner})

    assert reward_token.balanceOf(owner) == REWARD_PER_HOUR_FOR_ONE_TOKEN * HOURS_TO_PASS * 3
    assert staking.userStakeInfo(owner)[1] == 0

    

