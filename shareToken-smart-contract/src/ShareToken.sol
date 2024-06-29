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
    address[] public holders; 
    mapping(address => bool) public isHolder;
    mapping(address => mapping(address => uint256)) public allowance;


    uint256 public teamAllocation = (totalSupply * 30) / 100;
    uint256 public initialMint = (totalSupply * 20) / 100;
    uint256 public airdropMint = (totalSupply * 50) / 100;

    uint256 public unlockStart;
    uint256 public unlockedTokens = 0;

    address public owner;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event ProposalCreated(uint256 id, string title, uint256 snapshotId);
    event Voted(address indexed voter, uint256 proposalId, bool vote);

    struct Proposal {
        uint256 id;
        string title;
        string description;
        uint256 deadline;
        uint256 snapshotId;
        mapping(address => bool) hasVoted;
        mapping(address => bool) vote;
        mapping(address => uint256) votingPowers;
        uint256 totalYes;
        uint256 totalNo;
    }

    uint256 public nextProposalId;
    mapping(uint256 => Proposal) public proposals;

    constructor() {
        owner = msg.sender;
        balanceOf[projectWallet] = initialMint;
        balanceOf[address(this)] = 0;
        unlockStart = block.timestamp;
        remainingUnlockedTokens = teamAllocation;
        nextProposalId = 0;
        holders.push(msg.sender);
        isHolder[msg.sender] = true;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only contract owner can call this function");
        _;
    }

    function getContractAddress() public view returns (address) {
        return address(this);
    }

    function getBalance(address _address) public view returns (uint256) {
        return balanceOf[_address] / (10**uint256(decimals));
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function transfer(address _to, uint256 _value)
        public
        returns (bool success)
    {
        require(_to != address(0), "Invalid address");
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;

        if (!isHolder[_to]) {
            holders.push(_to);
            isHolder[_to] = true;
        }
        if (balanceOf[msg.sender] == 0) {
            isHolder[msg.sender] = false;
        }

        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_from != address(0), "Invalid address");
        require(_to != address(0), "Invalid address");
        require(balanceOf[_from] >= _value, "Insufficient balance");
        
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;

        if (!isHolder[_to]) {
            holders.push(_to);
            isHolder[_to] = true;
        }
        if (balanceOf[_from] == 0) {
            isHolder[_from] = false;
        }

        emit Transfer(_from, _to, _value);
        return true;
    }

    // vote  ------------------------------------------------------------------------------------------------------------
    function createProposal(string memory _title, string memory _description, uint256 _deadline) public onlyOwner {
        Proposal storage proposal = proposals[nextProposalId];
        proposal.id = nextProposalId;
        proposal.title = _title;
        proposal.description = _description;
        proposal.deadline = block.timestamp + _deadline;
        proposal.snapshotId = nextProposalId;

        for (uint256 i = 0; i < holders.length; i++) {
            address voter = holders[i];
            if (isHolder[voter]) { 
                proposal.votingPowers[voter] = balanceOf[voter]/10**uint256(decimals);
            }
        }

        emit ProposalCreated(nextProposalId, _title, nextProposalId);
        nextProposalId++;
    }

    function vote(uint256 _proposalId, bool _vote) public {
        Proposal storage proposal = proposals[_proposalId];
        require(block.timestamp < proposal.deadline, "Voting period has ended");
        require(!proposal.hasVoted[msg.sender], "Already voted");

        proposal.hasVoted[msg.sender] = true;
        proposal.vote[msg.sender] = _vote;
        if (_vote) {
            proposal.totalYes += proposal.votingPowers[msg.sender];
        } else {
            proposal.totalNo += proposal.votingPowers[msg.sender];
        }

        emit Voted(msg.sender, _proposalId, _vote);
    }

    function getProposal(uint256 _proposalId) public view returns (string memory title, string memory description, uint256 totalYes, uint256 totalNo) {
        Proposal storage proposal = proposals[_proposalId];
        return (proposal.title, proposal.description, proposal.totalYes, proposal.totalNo);
    }

    function listActiveProposals() public view returns (uint256[] memory, string[] memory, string[]memory, uint256[]memory, uint256[]memory, uint256[]memory ) {
        uint256 activeCount = 0;

        for (uint256 i = 0; i < nextProposalId; i++) {
            if (block.timestamp < proposals[i].deadline) {
                activeCount++;
            }
        }

        uint256[] memory ids = new uint256[](activeCount);
        string[] memory titles = new string[](activeCount);
        string[] memory descriptions = new  string[](activeCount);
        uint256[] memory totalYess = new uint256[](activeCount); 
        uint256[] memory totalNos = new uint256[](activeCount); 
        uint256[] memory remainingMinute = new uint256[](activeCount);

        uint256 currentIndex = 0;
        for (uint256 i = 0; i < nextProposalId; i++) {
            if (block.timestamp < proposals[i].deadline) {
                ids[currentIndex] = proposals[i].id;
                titles[currentIndex] = proposals[i].title;
                descriptions[currentIndex] = proposals[i].description;
                totalYess[currentIndex] = proposals[i].totalYes;
                totalNos[currentIndex] = proposals[i].totalNo;
                remainingMinute[currentIndex]=  (proposals[i].deadline - block.timestamp) / 60 ;
                currentIndex++;
            }
        }

        return (ids, titles, descriptions,  totalYess,  totalNos, remainingMinute);
    }

    function listEndProposals() public view returns (uint256[] memory, string[] memory, string[]memory, uint256[]memory, uint256[]memory ) {
        uint256 endCount = 0;

        for (uint256 i = 0; i < nextProposalId; i++) {
            if (block.timestamp > proposals[i].deadline) {
                endCount++;
            }
        }

        uint256[] memory ids = new uint256[](endCount);
        string[] memory titles = new string[](endCount);
        string[] memory descriptions = new  string[](endCount);
        uint256[] memory totalYess = new uint256[](endCount); 
        uint256[] memory totalNos = new uint256[](endCount); 

        uint256 currentIndex = 0;
        for (uint256 i = 0; i < nextProposalId; i++) {
            if (block.timestamp > proposals[i].deadline) {
                ids[currentIndex] = proposals[i].id;
                titles[currentIndex] = proposals[i].title;
                descriptions[currentIndex] = proposals[i].description;
                totalYess[currentIndex] = proposals[i].totalYes;
                totalNos[currentIndex] = proposals[i].totalNo;
                currentIndex++;
            }
        }

        return (ids, titles, descriptions,  totalYess,  totalNos);
    }

    function getVotersDetails(uint256 _proposalId) 
        public 
        view 
        returns (
            address[] memory, 
            uint256[] memory, 
            bool[] memory
        ) 
    {
        uint256 voterCount = 0;

        for (uint256 i = 0; i < holders.length; i++) {
            if (proposals[_proposalId].hasVoted[holders[i]]) {
                voterCount++;
            }
        }

        address[] memory voters = new address[](voterCount);
        uint256[] memory votingPowers = new uint256[](voterCount);
        bool[] memory votes = new bool[](voterCount);

        uint256 index = 0;
        for (uint256 i = 0; i < holders.length; i++) {
            if (proposals[_proposalId].hasVoted[holders[i]]) {
                voters[index] = holders[i];
                votingPowers[index] = proposals[_proposalId].votingPowers[holders[i]];
                votes[index] = proposals[_proposalId].vote[holders[i]];
                index++;
            }
        }

        return (voters, votingPowers, votes);
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
        uint256 timePassed = currentTime - unlockStart; //距離部署合約之後過了多久
        uint256 intervalsPassed = timePassed / (365 days / 2); //過了幾個半年

        if (intervalsPassed >= 10) {
            return (0, 0);
        } else {
            //計算距離下一次解鎖還有多久
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
        uint256 amountInWei = amount * 10**uint256(decimals);
        require(balanceOf[msg.sender] >= amountInWei, "Insufficient balance");

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