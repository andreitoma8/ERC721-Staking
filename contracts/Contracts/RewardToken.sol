// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

// Simple ERC721 Smart Contract made for Rewards.

contract RewardToken is ERC20 {
    constructor() ERC20("RewardToken", "RT") {
        _mint(msg.sender, 1000000 * 10**decimals());
    }
}
