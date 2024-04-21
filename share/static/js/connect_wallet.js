document.addEventListener("DOMContentLoaded", function () {
    var connectWalletBtn = document.getElementById("connectWalletBtn");
    var disconnectSelect = document.getElementById("disconnectSelect");
    var logoutBtn = document.getElementById("logoutBtn");
    localStorage.setItem('contract_address', '0x146dBaE602B862835797c82011cdFe1AbCcb46F0');

    function switchNetwork() {
        const chainId = '0x61'; //mainnet 0x38 testnet 0x61
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
                            rpcUrl: "https://rpc.ankr.com/bsc_testnet_chapel" 
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
});
