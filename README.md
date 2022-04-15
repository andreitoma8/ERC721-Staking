# ERC721Staking Smart Contract.
### The goal is to create a Smart Contract where users can Stake their ERC721 Tokens and Owner can distribute rewards.

### Smart Contract recieved a free exploratory audit by Marco form [Paladin Blockchain Security](https://paladinsec.co). All audit notes and issues can be found in their raw form over [here](https://gist.github.com/JorgeAtPaladin/cbbdd568925c3d86645509814f02ea32).
All issues and recommendations were addressed but:`INFO: userStakeInfo reverts for users with a zero stake. this is not desirable for UI purposes.`

Created using [OpenZeppelin](https://openzeppelin.com/)'s [ERC20](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol) and [ERC721](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol) Smart Contracts.

###### This iteration of a Staking Smart Contract for ERC721 is a separate one, so you will need three SC: one for your ERC721 Collection, one for your ERC20 Token and one for the Staking Pool. You will also have to send the ERC20 Token to the Staking Smart Contract so it will be able to pay rewards for your stakers. In the future I will create a ERC20 extension for ERC721 Staking so users will be able to mint ERC20 Tokens directly from the ERC20 SC based on ERC721 Stake. This will also make the developer job easier by only having to manage two Smart Contracts.

### Features for users:

1. Deposit your ERC721 Token/s and claim a fixed amount of ERC20 Tokens calculated hourly.
1. Withdraw your ERC721 Token/s.
1. Withdraw rewards.

### Features for owner:

1. Distribute ERC20 Token by ERC721 Tokens Locking(Staking).
1. Set a fixed hourly reward per ERC721 Token Locked(Staked).

### Prerequisites:

##### Rinkeby deployment
- [Python](https://www.python.org/downloads/)
- Brownie
```
python3 -m pip install --user pipx
python3 -m pipx ensurepath
# restart terminal
pipx install eth-brownie
```
- A free [Infura](https://infura.io/) Project Id key for Rinkeby Network

### Instalation 

Clone this repo:

```
git clone https://github.com/andreitoma8/ERC721-Staking
cd ERC721-Staking
```

### Deploy to Rinkeby

- Add a `.env` file with the same contents of `.env.example`, but replaced with your variables.

- Run the command:
```
brownie run scripts/deploy.py --network rinkeby
```
The script will:

1. Deploy the ERC20 Reward Token, mint 1.000.000 for yourself and verify the Smart Contract on .rinkeby.etherscan.io.
1. Deploy the ERC721 NFT Collection, mint 5 Tokens for yourself and verify the Smart Contract on .rinkeby.etherscan.io.
1. Deploy the ERC721 Staking Smart Contract and verify it on .rinkeby.etherscan.io.

##### Any feedback is much apreciated! 
##### If this was helpful please consider donating: 
`0xA4Ad17ef801Fa4bD44b758E5Ae8B2169f59B666F`

# Happy hacking!