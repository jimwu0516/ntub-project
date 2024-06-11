// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "forge-std/Test.sol";
import "../src/ShareToken.sol";

contract ShareTokenTest is Test {
    ShareToken shareToken;
    address owner;
    address addr1;
    address addr2;

    function setUp() public {
        owner = address(this);
        addr1 = address(0x1);
        addr2 = address(0x2);
        shareToken = new ShareToken();
    }

    function testInitialSettings() public {
        assertEq(shareToken.name(), "ShareToken");
        assertEq(shareToken.symbol(), "STE");
        assertEq(shareToken.decimals(), 18);
        assertEq(shareToken.totalSupply(), 10000000 * 10 ** 18);
        assertEq(shareToken.balanceOf(owner), shareToken.initialMint());
    }

    function testTransfer() public {
        uint256 ownerStartBalance = shareToken.balanceOf(owner);
        uint256 amount = 100 * 10 ** 18;

        vm.startPrank(owner);
        bool success = shareToken.transfer(addr1, amount);
        assert(success);

        assertEq(shareToken.balanceOf(owner), ownerStartBalance - amount);
        assertEq(shareToken.balanceOf(addr1), amount);
        vm.stopPrank();
    }

    function testTransferFail() public {
        uint256 amount = 100 * 10 ** 18;

        vm.startPrank(addr1);
        vm.expectRevert("Insufficient balance");
        shareToken.transfer(addr2, amount);
        vm.stopPrank();
    }

    function testCreateProposal() public {
        vm.prank(owner);
        shareToken.createProposal("Test Proposal", "Description", 7 days);

        (string memory title,,uint256 totalYes,uint256 totalNo) = shareToken.getProposal(0);
        assertEq(title, "Test Proposal");
        assertEq(totalYes, 0); 
        assertEq(totalNo, 0);  
    }

    function testVote() public {
        vm.prank(owner);
        shareToken.createProposal("Test Proposal", "Description", 7 days);
        vm.prank(owner);
        shareToken.vote(0, true);

        (,, uint256 totalYes,) = shareToken.getProposal(0);
        assertEq(totalYes, shareToken.balanceOf(owner) / (10 ** 18)); 
    }


    function testUnlockTokens() public {
        vm.warp(365 days); 

        vm.prank(owner);
        shareToken.unlockTokens();
        uint256 expectedBalance = shareToken.balanceOf(owner);
        assertTrue(expectedBalance > 0, "Should unlock tokens and increase owner balance");
    }


    function testReturnDepositAndAirdrop() public {
        vm.prank(owner);
        shareToken.returnDepositAndAirdrop(addr1, addr2, 100, 10, 50);

        assertEq(shareToken.balanceOf(addr1), 90 * 10 ** 18); 
        assertEq(shareToken.balanceOf(addr2), 60 * 10 ** 18); 
    }
}
