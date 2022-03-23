// SPDX-License-Identifier: MIT
// Creator: andreitoma8
pragma solidity ^0.8.4;

import "./Contracts/ERC721A.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC721/utils/ERC721Holder.sol";

contract ERC721Staking is ERC721A {
    using SafeERC20 for IERC20;

    // Interface for the rewards token
    IERC20 public rewardsToken;

    // Struct with Staker info
    struct Staker {
        // The amount of tokens staked
        uint256 amountStaked;
        // Last time of details update for Deposit
        uint256 timeOfLastUpdate;
        // Calculated, but unclaimed rewards. These are calculated
        // each time a user writes to the contract
        uint256 unclaimedRewards;
    }

    // Rewards per hour per token deposited in wei.
    uint256 private rewardsPerHour = 100000;

    // Mapping of addresses to Staker info
    mapping(address => Staker) stakers;
    // Mapping of tokenId to staker, so we know
    // who to send back the token to when unstaking
    mapping(uint256 => address) stakerAddress;

    // Args: name of the collection, symbol of the collection and the address of the reward token
    constructor(
        string memory _name,
        string memory _symbol,
        address _rewardsToken
    ) ERC721A(_name, _symbol) {
        rewardsToken = IERC20(_rewardsToken);
    }

    // If msg.sender already has NFTs staked, calculate his rewards and add them to unclaimedRewards
    // For every tokenId of the _tokenIds array check if msg.sender is the owner, transfer the token
    // to this contract, increment amountStaked of msg.sender and mapp his address to the tokenId to
    // be able to send it back on withdraw. Also reset lastTimeOfUpdate.
    function stake(uint256[] memory _tokenIds) public {
        if (stakers[msg.sender].amountStaked > 0) {
            uint256 rewards = calculateRewards(msg.sender);
            stakers[msg.sender].unclaimedRewards += rewards;
        }
        for (uint256 i; i < _tokenIds.length; ++i) {
            require(
                ownerOf(_tokenIds[i]) == msg.sender,
                "Can't stake token you don't own"
            );
            transferFrom(msg.sender, address(this), _tokenIds[i]);
            stakers[msg.sender].amountStaked++;
            stakerAddress[_tokenIds[i]] = msg.sender;
        }
        stakers[msg.sender].timeOfLastUpdate = block.timestamp;
    }

    // Check if the msg.sender has any tokens staked and if he is withdrawing more than he can.
    // Calculate user rewards and store them in unclaimedRewards.
    // For every element in the array chech if msg.sender is the rightful owner of the token with
    // the help of the stakerAddress mapping, decrement the amountStaked and transfer the token
    // back to the msg.sender.
    function unstake(uint256[] memory _tokenIds) public {
        require(
            stakers[msg.sender].amountStaked > 0,
            "You have no tokens staked"
        );
        require(
            _tokenIds.length <= stakers[msg.sender].amountStaked,
            "You tried to unstake too many tokens!"
        );
        uint256 rewards = calculateRewards(msg.sender);
        stakers[msg.sender].unclaimedRewards += rewards;
        for (uint256 i; i < _tokenIds.length; ++i) {
            require(stakerAddress[_tokenIds[i]] == msg.sender);
            stakers[msg.sender].amountStaked--;
            transferFrom(address(this), msg.sender, _tokenIds[i]);
        }
        stakers[msg.sender].timeOfLastUpdate = block.timestamp;
    }

    // Calculates the rewards accumulated since the last timeOfLastUpdate
    // for msg.sender, adds the unclaimedRewards and resets the two
    // values before sending the tokens to the msg.sender
    function claimRewards() public {
        uint256 rewards = calculateRewards(msg.sender) +
            stakers[msg.sender].unclaimedRewards;
        require(rewards > 0, "You have no rewards to claim");
        stakers[msg.sender].timeOfLastUpdate = block.timestamp;
        stakers[msg.sender].unclaimedRewards = 0;
        rewardsToken.transfer(msg.sender, rewards);
    }

    // View function that returns the total available rewards for a user
    function availableRewards(address _user) public view returns (uint256) {
        uint256 _rewards = stakers[_user].unclaimedRewards +
            calculateRewards(_user);
        return _rewards;
    }

    // Internal function that calculates rewards as staked hours
    // since the timeOfLastUpdate multilyed by number of NFTs staked
    // multiplyed by the rewardTokens rewarded per hour for one NFT
    function calculateRewards(address _staker)
        internal
        view
        returns (uint256 _rewards)
    {
        return (
            ((
                (((block.timestamp - stakers[_staker].timeOfLastUpdate) /
                    3600) * stakers[msg.sender].amountStaked)
            ) * rewardsPerHour)
        );
    }
}
