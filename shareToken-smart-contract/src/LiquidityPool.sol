// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IShareToken {
    function transferFrom(address from, address to, uint256 value) external returns (bool);
    function transfer(address to, uint256 value) external returns (bool);
    function balanceOf(address owner) external view returns (uint256);
}

interface IFakeUSDT {
    function transferFrom(address from, address to, uint256 value) external returns (bool);
    function transfer(address to, uint256 value) external returns (bool);
    function balanceOf(address owner) external view returns (uint256);
}

contract LiquidityPool {
    IShareToken public shareToken;
    IFakeUSDT public usdtToken;

    uint256 public shareTokenReserve;
    uint256 public usdtTokenReserve;

    mapping(address => uint256) public liquidity;
    uint256 public totalLiquidity;

    event AddLiquidity(address indexed provider, uint256 shareTokenAmount, uint256 usdtTokenAmount);
    event RemoveLiquidity(address indexed provider, uint256 shareTokenAmount, uint256 usdtTokenAmount);
    event Swap(address indexed user, string tokenOut, uint256 amountOut, uint256 amountIn);

    constructor(address _shareTokenAddress, address _usdtTokenAddress) {
        shareToken = IShareToken(_shareTokenAddress);
        usdtToken = IFakeUSDT(_usdtTokenAddress);
    }

    function addLiquidity(uint256 _shareTokenAmount, uint256 _usdtTokenAmount) public {
        require(_shareTokenAmount > 0 && _usdtTokenAmount > 0, "Invalid amount");

        uint256 liquidityMinted;
        if (totalLiquidity == 0) {
            liquidityMinted = _shareTokenAmount;
        } else {
            uint256 shareTokenRatio = (_shareTokenAmount * totalLiquidity) / shareTokenReserve;
            uint256 usdtTokenRatio = (_usdtTokenAmount * totalLiquidity) / usdtTokenReserve;
            require(shareTokenRatio == usdtTokenRatio, "Invalid token ratio");
            liquidityMinted = shareTokenRatio;
        }

        shareToken.transferFrom(msg.sender, address(this), _shareTokenAmount);
        usdtToken.transferFrom(msg.sender, address(this), _usdtTokenAmount);

        shareTokenReserve += _shareTokenAmount;
        usdtTokenReserve += _usdtTokenAmount;

        liquidity[msg.sender] += liquidityMinted;
        totalLiquidity += liquidityMinted;

        emit AddLiquidity(msg.sender, _shareTokenAmount, _usdtTokenAmount);
    }

    function calculateRequiredUSDT(uint256 shareTokenAmount) public view returns (uint256) {
        require(shareTokenAmount > 0, "Invalid shareToken amount");
        return (shareTokenAmount * usdtTokenReserve) / shareTokenReserve;
    }

    function calculateRequiredShareToken(uint256 usdtAmount) public view returns (uint256) {
        require(usdtAmount > 0, "Invalid USDT amount");
        return (usdtAmount * shareTokenReserve) / usdtTokenReserve;
    }

    function removeLiquidity(uint256 _liquidityAmount) public {
        require(_liquidityAmount > 0, "Invalid amount");
        require(liquidity[msg.sender] >= _liquidityAmount, "Insufficient liquidity");

        uint256 shareTokenAmount = (_liquidityAmount * shareTokenReserve) / totalLiquidity;
        uint256 usdtTokenAmount = (_liquidityAmount * usdtTokenReserve) / totalLiquidity;

        shareTokenReserve -= shareTokenAmount;
        usdtTokenReserve -= usdtTokenAmount;

        liquidity[msg.sender] -= _liquidityAmount;
        totalLiquidity -= _liquidityAmount;

        shareToken.transfer(msg.sender, shareTokenAmount);
        usdtToken.transfer(msg.sender, usdtTokenAmount);

        emit RemoveLiquidity(msg.sender, shareTokenAmount, usdtTokenAmount);
    }

    function swapShareTokenForUSDT(uint256 _shareTokenAmount) public {
        require(_shareTokenAmount > 0, "Invalid amount");
        uint256 usdtAmountOut = getAmountOut(_shareTokenAmount, shareTokenReserve, usdtTokenReserve);

        shareToken.transferFrom(msg.sender, address(this), _shareTokenAmount);
        usdtToken.transfer(msg.sender, usdtAmountOut);

        shareTokenReserve += _shareTokenAmount;
        usdtTokenReserve -= usdtAmountOut;

        emit Swap(msg.sender, "USDT", usdtAmountOut, _shareTokenAmount);
    }

    function getSwapShareTokenForUSDT(uint256 _shareTokenAmount) public view returns (uint256) {
        require(_shareTokenAmount > 0, "Invalid amount");
        uint256 usdtAmountOut = getAmountOut(_shareTokenAmount, shareTokenReserve, usdtTokenReserve);
        return usdtAmountOut;
    }

    function swapUSDTForShareToken(uint256 _usdtAmount) public {
        require(_usdtAmount > 0, "Invalid amount");
        uint256 shareTokenAmountOut = getAmountOut(_usdtAmount, usdtTokenReserve, shareTokenReserve);

        usdtToken.transferFrom(msg.sender, address(this), _usdtAmount);
        shareToken.transfer(msg.sender, shareTokenAmountOut);

        usdtTokenReserve += _usdtAmount;
        shareTokenReserve -= shareTokenAmountOut;

        emit Swap(msg.sender, "ShareToken", shareTokenAmountOut, _usdtAmount);
    }

    function getSwapUSDTForShareToken(uint256 _usdtAmount) public view returns (uint256) {
        require(_usdtAmount > 0, "Invalid amount");
        uint256 shareTokenAmountOut = getAmountOut(_usdtAmount, usdtTokenReserve, shareTokenReserve);
        return shareTokenAmountOut;
    }

    function getUserLiquidity() public view returns (uint256) {
        return liquidity[msg.sender];
    }

    function getAmountOut(uint256 _amountIn, uint256 _reserveIn, uint256 _reserveOut) private pure returns (uint256) {
        require(_amountIn > 0, "Invalid input amount");
        uint256 amountInWithFee = _amountIn * 997;
        uint256 numerator = amountInWithFee * _reserveOut;
        uint256 denominator = (_reserveIn * 1000) + amountInWithFee;
        return numerator / denominator;
    }
}
