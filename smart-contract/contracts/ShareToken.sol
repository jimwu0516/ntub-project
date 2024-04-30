// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract ShareToken {
    string public name = "ShareToken";
    string public symbol = "STE";
    uint8 public decimals = 18;
    uint256 public totalSupply = 10000000 * 10**uint256(decimals);
    uint256 public remainingUnlockedTokens;

    address public projectWallet = msg.sender;

    mapping(address => uint256) public balanceOf;

    uint256 public teamAllocation = (totalSupply * 30) / 100;
    uint256 public initialMint = (totalSupply * 20) / 100;
    uint256 public airdropMint = (totalSupply * 50) / 100;

    uint256 public unlockStart;
    uint256 public unlockedTokens = 0;

    address public owner;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor() {
        owner = msg.sender;
        balanceOf[projectWallet] = initialMint;
        balanceOf[address(this)] = 0;
        unlockStart = block.timestamp;
        remainingUnlockedTokens = teamAllocation;
    }

    modifier onlyOwner() {
        require(
            msg.sender == owner,
            "Only contract owner can call this function"
        );
        _;
    }

    function getContractAddress() public view returns (address) {
        return address(this);
    }

    function getBalance(address _address) public view returns (uint256) {
        return balanceOf[_address] / (10**uint256(decimals));
    }

    function transfer(address _to, uint256 _value)
        public
        returns (bool success)
    {
        require(_to != address(0), "Invalid address");
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    //unlocktoken-----------------------------------------------------------------------------------------------------------------------------------
    function unlockTokens() external onlyOwner {
        require(block.timestamp >= unlockStart, "Tokens are still locked");
        require(unlockedTokens < teamAllocation, "All tokens unlocked");

        uint256 currentTime = block.timestamp;
        uint256 timePassed = currentTime - unlockStart;
        uint256 intervalsPassed = timePassed / (365 days / 2);

        uint256[] memory unlockAmounts = new uint256[](10);
        unlockAmounts[0] = 0 * (10**uint256(decimals));
        unlockAmounts[1] = 93706 * (10**uint256(decimals));
        unlockAmounts[2] = 121818 * (10**uint256(decimals));
        unlockAmounts[3] = 158363 * (10**uint256(decimals));
        unlockAmounts[4] = 205872 * (10**uint256(decimals));
        unlockAmounts[5] = 267634 * (10**uint256(decimals));
        unlockAmounts[6] = 347924 * (10**uint256(decimals));
        unlockAmounts[7] = 452301 * (10**uint256(decimals));
        unlockAmounts[8] = 587992 * (10**uint256(decimals));
        unlockAmounts[9] = 764390 * (10**uint256(decimals));

        if (intervalsPassed > unlockedTokens) {
            uint256 tokensToUnlock = 0;
            for (uint256 i = unlockedTokens; i < intervalsPassed; i++) {
                tokensToUnlock += unlockAmounts[i];
            }
            unlockedTokens = intervalsPassed;
            balanceOf[projectWallet] += tokensToUnlock;
            remainingUnlockedTokens -= tokensToUnlock;
            emit Transfer(address(this), projectWallet, tokensToUnlock);
        }
    }

    function nextUnlock() external view returns (uint256 day, uint256 hour) {
        require(block.timestamp >= unlockStart, "Tokens are still locked");

        uint256 currentTime = block.timestamp;
        uint256 timePassed = currentTime - unlockStart; //How long has it been since the deployment of the contract
        uint256 intervalsPassed = timePassed / (365 days / 2); //How many half-years have passed

        if (intervalsPassed >= 10) {
            return (0, 0);
        } else {
            //Calculate how much time is left until the next unlock
            uint256 timeUntilUnlock = (intervalsPassed + 1) *
                (365 days / 2) -
                timePassed;
            day = timeUntilUnlock / 1 days;
            hour = (timeUntilUnlock % 1 days) / 1 hours;
            return (day, hour);
        }
    }

    //paydeposit tackle -----------------------------------------------------------------------------------------------------------------------------------
    function payDeposit(uint256 amount) public returns (bool success) {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");

        uint256 amountInWei = amount * 10**uint256(decimals);

        balanceOf[msg.sender] -= amountInWei;
        balanceOf[projectWallet] += amountInWei;

        emit Transfer(msg.sender, projectWallet, amountInWei);

        return true;
    }
    
    //return deposit and airdrop token ---------------------------------
    function returnDepositAndAirdrop(
        address borrower_address,
        address contributor_address,
        uint256 depositAmount,
        uint256 damagePercentage,
        uint256 airdropAmount
    ) public onlyOwner {
        require(
            borrower_address != address(0) && contributor_address != address(0),
            "Invalid address"
        );
        require(
            damagePercentage >= 0 && damagePercentage <= 100,
            "Invalid fraction percentage"
        );
        require(
            balanceOf[projectWallet] >= depositAmount,
            "Insufficient balance in project wallet"
        );
        require(
            airdropAmount > 0, "Invalid amount"
        );

        uint256 depositAmountInWei = depositAmount * 10**uint256(decimals);
        uint256 contributorAmount = (depositAmountInWei * damagePercentage) / 100;
        uint256 borrowerAmount = depositAmountInWei - contributorAmount;

        uint256 airdropAmountInWei = airdropAmount * 10**uint256(decimals);

        balanceOf[projectWallet] -= depositAmountInWei;
        balanceOf[contributor_address] += contributorAmount;
        balanceOf[borrower_address] += borrowerAmount;

        emit Transfer(projectWallet, contributor_address, contributorAmount);
        emit Transfer(projectWallet, borrower_address, borrowerAmount);

        //-----------------airdrop---------------------
        if (airdropAmountInWei <= airdropMint) {
            airdropMint -= airdropAmountInWei;
            balanceOf[contributor_address] += airdropAmountInWei;
            emit Transfer(address(this), contributor_address, airdropAmountInWei);
        } else {
            require(
                balanceOf[projectWallet] >= airdropAmountInWei,
                "Insufficient balance in project wallet"
            );
            balanceOf[projectWallet] -= airdropAmountInWei;
            balanceOf[contributor_address] += airdropAmountInWei;
            emit Transfer(projectWallet, contributor_address, airdropAmountInWei);
        }
    }


    //return deposit while borrower_not_picked_up ---------------------------------
    function borrowerNotPickedUpReturnDeposit(
        address borrower_address,
        address contributor_address,
        uint256 depositAmount
    ) public onlyOwner {
        require(
            borrower_address != address(0) && contributor_address != address(0),
            "Invalid address"
        );
        require(
            balanceOf[projectWallet] >= depositAmount,
            "Insufficient balance in project wallet"
        );

        uint256 depositAamountInWei = depositAmount * 10**uint256(decimals);
        uint256 contributorAmount = (depositAamountInWei * 30) / 100;
        uint256 borrowerAmount = depositAamountInWei - contributorAmount;

        balanceOf[projectWallet] -= depositAamountInWei;
        balanceOf[contributor_address] += contributorAmount;
        balanceOf[borrower_address] += borrowerAmount;

        emit Transfer(projectWallet, contributor_address, contributorAmount);
        emit Transfer(projectWallet, borrower_address, borrowerAmount);
    }

    //return deposit while cancel_order ---------------------------------
    function cancelOrderReturnDeposit(
        address borrower_address,
        uint256 depositAmount
    ) public onlyOwner {
        require(
            borrower_address != address(0) ,
            "Invalid address"
        );
        require(
            balanceOf[projectWallet] >= depositAmount,
            "Insufficient balance in project wallet"
        );

        uint256 depositAamountInWei = depositAmount * 10**uint256(decimals);
        
        balanceOf[projectWallet] -= depositAamountInWei;
        balanceOf[borrower_address] += depositAamountInWei;

        emit Transfer(projectWallet, borrower_address, depositAamountInWei);
    }     

}
