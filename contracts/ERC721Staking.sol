// SPDX-License-Identifier: MIT
// Creator: andreitoma8
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/token/ERC721/utils/ERC721Holder.sol";

contract ERC721Staking is ERC721Holder {
    using SafeERC20 for IERC20;

    IERC20 public rewardsToken;
    IERC721 public nftCollection;

    struct Staker {
        uint256 amountStaked;
        uint256 timeOfLastUpdate;
        uint256 unclaimedRewards;
    }

    // Rewards per hour per token deposited in wei.
    uint256 private rewardsPerHour = 100000;

    mapping(address => Staker) stakers;
    mapping(uint256 => address) stakerAddress;

    constructor(
        address _nftCollection,
        address _rewardsToken
    ) {
        nftCollection = IERC721(_nftCollection);
        rewardsToken = IERC20(_rewardsToken);
    }

    function stake(uint256[] memory _tokenIds) public {
        if (stakers[msg.sender].amountStaked > 0) {
            uint256 rewards = calculateRewards(msg.sender);
            stakers[msg.sender].unclaimedRewards += rewards;
        }
        for (uint256 i; i < _tokenIds.length; ++i) {
            nftCollection.transferFrom(msg.sender, address(this), _tokenIds[i]);
            stakers[msg.sender].amountStaked++;
            stakerAddress[_tokenIds[i]] = msg.sender;
        }
        stakers[msg.sender].timeOfLastUpdate = block.timestamp;
    }

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
            nftCollection.transferFrom(address(this), msg.sender, _tokenIds[i]);
        }
        stakers[msg.sender].timeOfLastUpdate = block.timestamp;
    }

    function claimRewards() public {
        uint256 rewards = calculateRewards(msg.sender) +
            stakers[msg.sender].unclaimedRewards;
        require(rewards > 0, "You have no rewards to claim");
        stakers[msg.sender].unclaimedRewards = 0;
        rewardsToken.transfer(msg.sender, rewards);
    }

    // View

    function availableRewards(address _user) public view returns (uint256) {
        require(stakers[_user].amountStaked > 0, "User has no tokens staked");
        uint256 _rewards = stakers[_user].unclaimedRewards +
            calculateRewards(_user);
        return _rewards;
    }

    

    // Internal

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
