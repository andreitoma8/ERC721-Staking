// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

// Simple ERC721 Smart Contract made for Rewards.

contract RewardToken is ERC20 {
    constructor(string memory _name, string memory _symbol)
        ERC20(_name, _symbol)
    {

    }

    function mint(address _user, uint256 _amount) public {
        _mint(_user, _amount);
    }
}
