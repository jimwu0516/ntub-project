document.addEventListener("DOMContentLoaded", function () {
    var connectWalletBtn = document.getElementById("connectWalletBtn");
    var disconnectSelect = document.getElementById("disconnectSelect");
    var logoutBtn = document.getElementById("logoutBtn");
    localStorage.setItem('contract_address', '0xec0888881eFf7040FF4207853F4E2bA28310401B');
    var rpcUrl = "https://rpc.ankr.com/bsc_testnet_chapel"
    const chainId = '0x61'; //mainnet 0x38 testnet 0x61

    function switchNetwork() {
        window.ethereum.request({
            method: 'wallet_switchEthereumChain',
            params: [{ chainId: chainId }]
        }).catch((switchError) => {
            if (switchError.code === 4902) {
                try {
                    window.ethereum.request({
                        method: 'wallet_addEthereumChain',
                        params: [{
                            chainId: chainId,
                            rpcUrl: rpcUrl
                        }]
                    });
                } catch (addError) {
                    console.error('Failed to add the network:', addError);
                }
            } else {
                console.error('Failed to switch the network:', switchError);
            }
        });
    }

    var isConnectedAddress = localStorage.getItem('walletConnected');
    if (isConnectedAddress) {
        connectWalletBtn.style.display = 'none';
        disconnectSelect.style.display = 'inline-block';
        disconnectSelect.innerHTML = `<option value="connect" selected>${isConnectedAddress.substring(0, 9)}...</option><option value="disconnect">中斷連接錢包</option>`;
    }

    connectWalletBtn.addEventListener("click", function () {
        if (typeof window.ethereum !== 'undefined') {
            window.ethereum.request({ method: 'wallet_requestPermissions', params: [{ eth_accounts: {} }] })
                .then(function () {
                    window.ethereum.request({ method: 'eth_requestAccounts' })
                        .then(function (accounts) {
                            var walletAddress = accounts[0];
                            localStorage.setItem('walletConnected', walletAddress);
                            connectWalletBtn.style.display = 'none';
                            disconnectSelect.style.display = 'inline-block';
                            disconnectSelect.innerHTML = `<option value="connect" selected>${walletAddress.substring(0, 9)}...</option><option value="disconnect">中斷連接錢包</option>`;
                            switchNetwork();
                        })
                        .catch(function (error) {
                            console.error(error);
                        });
                })
                .catch(function (error) {
                    console.error(error);
                });
        } else {
            alert("Metamask未安裝！！！");
        }
    });

    function disconnect() {
        localStorage.removeItem('walletConnected');
        connectWalletBtn.style.display = 'inline-block';
        disconnectSelect.style.display = 'none';
        connectWalletBtn.innerText = "Connect Wallet";
    }

    disconnectSelect.addEventListener("change", function () {
        if (disconnectSelect.value === 'disconnect') {
            disconnect();
        }
    });

    logoutBtn.addEventListener("click", function () {
        if (localStorage.getItem('walletConnected')) {
            disconnect();
        }
    });

    connectWalletBtn.addEventListener('mouseover', function () {
        connectWalletBtn.style.backgroundColor = "red";
        connectWalletBtn.style.transform = "scale(1.1)";
    });

    connectWalletBtn.addEventListener('mouseout', function () {
        connectWalletBtn.style.backgroundColor = "green";
        connectWalletBtn.style.transform = "scale(1)";
    });

    //-----------------------------------------------------------------------------------------------------------------------------
    const addNetworkBtn = document.getElementById("addNetworkBtn");

    addNetworkBtn.addEventListener("click", function () {
        if (typeof window.ethereum !== 'undefined') {
            ethereum
                .request({ method: 'eth_requestAccounts' })
                .then((accounts) => {
                    if (ethereum.networkVersion !== '97') {
                        ethereum
                            .request({
                                method: 'wallet_addEthereumChain',
                                params: [
                                    {
                                        chainId: chainId,
                                        chainName: 'Binance Smart Chain Testnet',
                                        rpcUrls: [rpcUrl],
                                        blockExplorerUrls: ['https://testnet.bscscan.com/'],
                                        nativeCurrency: {
                                            name: 'BNB',
                                            symbol: 'BNB',
                                            decimals: 18
                                        }
                                    }
                                ]
                            })
                            .then(() => {
                                console.log('BSC Testnet added')
                                addTokenToWallet()
                            })
                            .catch((error) => {
                                console.error(error)
                            })
                    } else {
                        addTokenToWallet()
                    }
                })
                .catch((error) => {
                    console.error(error)
                })

        } else {
            alert("Metamask未安裝！！！");
        }


    })



    function addTokenToWallet() {
        ethereum
            .request({
                method: 'wallet_watchAsset',
                params: {
                    type: 'ERC20',
                    options: {
                        address: localStorage.getItem('contract_address'),
                        symbol: 'STE',
                        decimals: 18,
                        image: ''
                    }
                }
            })
            .then((isAdded) => {
                if (isAdded) {
                    console.log('Token is already added to wallet')
                } else {
                    console.log('Token is not added to wallet')
                    ethereum
                        .request({
                            method: 'wallet_watchAsset',
                            params: {
                                type: 'ERC20',
                                options: {
                                    address: localStorage.getItem('contract_address'),
                                    symbol: 'STE',
                                    decimals: 18,
                                    image: ''
                                }
                            }
                        })
                        .then((success) => {
                            if (success) {
                                console.log('Token added to wallet')
                            } else {
                                console.log('Failed to add token to wallet')
                            }
                        })
                        .catch((error) => {
                            console.error(error)
                        })
                }
            })
            .catch((error) => {
                console.error('Error checking token in wallet:', error)
            })
    }
});
