

import os
from urllib.parse import urlparse

from eth_tester import EthereumTester
from eth_tester import PyEVMBackend
from web3 import WebsocketProvider, HTTPProvider, IPCProvider
from web3.exceptions import InfuraKeyNotFound
from web3.providers.eth_tester.main import EthereumTesterProvider

from nucypher.blockchain.eth.clients import NuCypherGethDevProcess


class ProviderError(Exception):
    pass


def _get_IPC_provider(provider_uri):
    uri_breakdown = urlparse(provider_uri)
    from nucypher.blockchain.eth.interfaces import BlockchainInterface
    return IPCProvider(ipc_path=uri_breakdown.path,
                       timeout=BlockchainInterface.TIMEOUT,
                       request_kwargs={'timeout': BlockchainInterface.TIMEOUT})


def _get_HTTP_provider(provider_uri):
    from nucypher.blockchain.eth.interfaces import BlockchainInterface
    return HTTPProvider(endpoint_uri=provider_uri, request_kwargs={'timeout': BlockchainInterface.TIMEOUT})


def _get_websocket_provider(provider_uri):
    from nucypher.blockchain.eth.interfaces import BlockchainInterface
    return WebsocketProvider(endpoint_uri=provider_uri, websocket_kwargs={'timeout': BlockchainInterface.TIMEOUT})


def _get_infura_provider(provider_uri):
    # https://web3py.readthedocs.io/en/latest/providers.html#infura-mainnet

    uri_breakdown = urlparse(provider_uri)
    infura_envvar = 'WEB3_INFURA_PROJECT_ID'
    os.environ[infura_envvar] = os.environ.get(infura_envvar, uri_breakdown.netloc)

    try:
        # TODO: Only testnet for now - #1496
        from web3.auto.infura.goerli import w3

    except InfuraKeyNotFound:
        raise ProviderError(f'{infura_envvar} must be provided in order to use an Infura Web3 provider {provider_uri}.')

    # Verify Connection
    connected = w3.isConnected()
    if not connected:
        raise ProviderError(f'Failed to connect to Infura node "{provider_uri}".')

    return w3.provider


def _get_auto_provider(provider_uri):
    from web3.auto import w3
    # how-automated-detection-works: https://web3py.readthedocs.io/en/latest/providers.html
    connected = w3.isConnected()
    if not connected:
        raise ProviderError('Cannot auto-detect node.  Provide a full URI instead.')
    return w3.provider


def _get_tester_pyevm(provider_uri):
    # https://web3py.readthedocs.io/en/latest/providers.html#httpprovider
    from nucypher.utilities.sandbox.constants import PYEVM_GAS_LIMIT, NUMBER_OF_ETH_TEST_ACCOUNTS

    # Initialize
    genesis_params = PyEVMBackend._generate_genesis_params(overrides={'gas_limit': PYEVM_GAS_LIMIT})
    pyevm_backend = PyEVMBackend(genesis_parameters=genesis_params)
    pyevm_backend.reset_to_genesis(genesis_params=genesis_params, num_accounts=NUMBER_OF_ETH_TEST_ACCOUNTS)

    # Test provider entry-point
    eth_tester = EthereumTester(backend=pyevm_backend, auto_mine_transactions=True)
    provider = EthereumTesterProvider(ethereum_tester=eth_tester)

    return provider


def _get_test_geth_parity_provider(provider_uri):
    from nucypher.blockchain.eth.interfaces import BlockchainInterface

    # geth --dev
    geth_process = NuCypherGethDevProcess()
    geth_process.start()
    geth_process.wait_for_ipc(timeout=30)
    provider = IPCProvider(ipc_path=geth_process.ipc_path, timeout=BlockchainInterface.TIMEOUT)

    BlockchainInterface.process = geth_process
    return provider


def _get_tester_ganache(provider_uri=None):
    endpoint_uri = provider_uri or 'http://localhost:7545'
    return HTTPProvider(endpoint_uri=endpoint_uri)
