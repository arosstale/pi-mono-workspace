"""
Ethereum whale monitor using Etherscan API (free tier)
"""

import os
import requests
import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from database import WhaleDatabase

# Known DEX and protocol addresses on ETH
DEX_PROTOCOLS = {
    'uniswap_v2': '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D',
    'uniswap_v3': '0xE592427A0AEce92De3Edee1F18E0157C05861564',
    '1inch': '0x111111125421cA6dc452d289314280a0e88F2A54',
    'sushiswap': '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F',
    'curve': '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',
}

# Known whale wallets (starting seed list - can be expanded)
INITIAL_WHALES_ETH = [
    '0x47ac0Fb4F2D84898e4D9E7b4DaB3C24507a6D503',  # Binance Wallet
    '0x28C6c06298d514Db089934071355E5743bf21d60',  # Binance 2
    '0xD6dF9934470ed36d183d11D80a7039351C5d5031',  # Another large wallet
    '0x21a31Ee1afC51d94C2eFCAa0820f1d56E5F3C109',  # Bitfinex
]

class EthereumWhaleMonitor:
    """Monitor Ethereum whale transactions using Etherscan API"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ETHERSCAN_API_KEY', '')
        self.base_url = 'https://api.etherscan.io/api'
        self.db = WhaleDatabase()
        self.min_eth_threshold = 10.0  # Minimum ETH to track
        self.min_usd_threshold = 100_000  # Minimum USD value to track

    def _make_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make API request with rate limiting"""
        params['apikey'] = self.api_key
        time.sleep(0.21)  # Rate limit: ~5 calls/second

        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get('status') != '1':
                print(f"API Error: {data.get('message', 'Unknown error')}")
                return None

            return data
        except Exception as e:
            print(f"Request failed: {e}")
            return None

    def get_latest_block(self) -> Optional[int]:
        """Get latest block number"""
        params = {'module': 'proxy', 'action': 'eth_blockNumber'}
        data = self._make_request(params)
        if data:
            return int(data.get('result', '0x0'), 16)
        return None

    def get_address_transactions(self, address: str, start_block: int = 0, end_block: int = 99999999) -> List[Dict[str, Any]]:
        """Get normal transactions for an address"""
        params = {
            'module': 'account',
            'action': 'txlist',
            'address': address,
            'startblock': start_block,
            'endblock': end_block,
            'sort': 'desc',
        }
        data = self._make_request(params)
        if data:
            return data.get('result', [])
        return []

    def get_eth_price(self) -> float:
        """Get current ETH price in USD"""
        params = {
            'module': 'proxy',
            'action': 'eth_getPrice',
        }
        data = self._make_request(params)
        if data and data.get('result'):
            return float(data['result'])
        return 0

    def _identify_tx_type(self, tx: Dict[str, Any]) -> tuple[str, Optional[str]]:
        """Identify transaction type and protocol"""
        to_address = tx.get('to', '').lower()
        input_data = tx.get('input', '0x')

        # Check for DEX interactions
        for protocol, addr in DEX_PROTOCOLS.items():
            if to_address == addr.lower():
                return 'swap', protocol

        # Check for contract interaction
        if input_data and input_data != '0x' and len(input_data) > 10:
            # Try to identify method selector (first 10 chars)
            method = input_data[:10]
            # Common DeFi method signatures
            known_methods = {
                '0x095ea7b3': 'approve',
                '0x38ed1739': 'swapExactTokensForTokens',
                '0x8803dbee': 'swapTokensForExactTokens',
                '0x7ff36ab5': 'swapExactETHForTokens',
                '0x18cbafe5': 'swapExactTokensForETH',
                '0xa9059cbb': 'transfer',
            }
            return known_methods.get(method, 'contract'), None

        # Regular transfer
        if tx.get('value', '0x0') != '0x0':
            return 'transfer', None

        return 'contract', None

    def _is_whale_transaction(self, tx: Dict[str, Any], eth_price: float) -> bool:
        """Check if transaction meets whale criteria"""
        # Convert hex value to ETH
        value_wei = int(tx.get('value', '0x0'), 16)
        value_eth = value_wei / 1e18
        value_usd = value_eth * eth_price

        # Check thresholds
        if value_eth >= self.min_eth_threshold or value_usd >= self.min_usd_threshold:
            return True

        return False

    def monitor_wallet(self, address: str, lookback_hours: int = 24) -> List[Dict[str, Any]]:
        """Monitor a single wallet for whale transactions"""
        print(f"Monitoring ETH wallet: {address}")

        # Calculate block range
        current_block = self.get_latest_block()
        if not current_block:
            print("Could not get latest block")
            return []

        # Ethereum blocks are ~13 seconds, so ~6600 blocks per day
        blocks_to_scan = int((lookback_hours / 24) * 6600)
        start_block = max(0, current_block - blocks_to_scan)

        txs = self.get_address_transactions(address, start_block, current_block)
        eth_price = self.get_eth_price()

        whale_txs = []
        for tx in txs:
            value_wei = int(tx.get('value', '0x0'), 16)
            value_eth = value_wei / 1e18
            value_usd = value_eth * eth_price

            if self._is_whale_transaction(tx, eth_price):
                tx_type, protocol = self._identify_tx_type(tx)

                tx_data = {
                    'tx_hash': tx['hash'],
                    'from_address': tx['from'],
                    'to_address': tx.get('to', '0x0'),
                    'value_eth': value_eth,
                    'value_usd': value_usd,
                    'gas_used': int(tx.get('gasUsed', '0'), 16),
                    'gas_price': tx.get('gasPrice'),
                    'tx_type': tx_type,
                    'protocol': protocol,
                    'block_number': int(tx['blockNumber'], 16),
                    'timestamp': int(tx['timeStamp']),
                }

                # Store in database
                tx_id = self.db.insert_eth_tx(tx_data)
                tx_data['id'] = tx_id
                whale_txs.append(tx_data)

                # Update whale wallet record
                self.db.insert_whale_wallet(tx['from'], 'eth', value_usd)
                if tx.get('to'):
                    self.db.insert_whale_wallet(tx['to'], 'eth', value_usd)

                # Generate alert for very large transfers
                if value_eth >= 100 or value_usd >= 500_000:
                    self.db.insert_whale_alert({
                        'alert_type': 'large_transfer',
                        'chain': 'eth',
                        'address': tx['from'],
                        'amount': value_eth,
                        'currency': 'ETH',
                        'description': f'Large transfer: {value_eth:.2f} ETH (${value_usd:,.0f}) via {protocol or tx_type}',
                    })

        print(f"  Found {len(whale_txs)} whale transactions")
        return whale_txs

    def monitor_whales(self, addresses: List[str] = None, lookback_hours: int = 24) -> Dict[str, Any]:
        """Monitor multiple whale wallets"""
        addresses = addresses or INITIAL_WHALES_ETH
        all_whale_txs = []

        print(f"Monitoring {len(addresses)} ETH wallets for last {lookback_hours} hours")

        for address in addresses:
            whale_txs = self.monitor_wallet(address, lookback_hours)
            all_whale_txs.extend(whale_txs)
            time.sleep(0.3)  # Be nice to the API

        return {
            'wallets_monitored': len(addresses),
            'whale_transactions': len(all_whale_txs),
            'transactions': all_whale_txs,
        }

    def scan_large_blocks(self, num_blocks: int = 100, eth_price: float = None) -> List[Dict[str, Any]]:
        """Scan recent blocks for large transactions"""
        if eth_price is None:
            eth_price = self.get_eth_price()

        current_block = self.get_latest_block()
        if not current_block:
            return []

        whale_txs = []
        print(f"Scanning last {num_blocks} blocks for large transactions")

        for block_num in range(current_block, current_block - num_blocks, -1):
            # Get block transactions
            params = {
                'module': 'proxy',
                'action': 'eth_getBlockByNumber',
                'tag': hex(block_num),
                'boolean': 'true',
            }
            data = self._make_request(params)

            if data and data.get('result'):
                block = data['result']
                txs = block.get('transactions', [])

                for tx in txs:
                    value_wei = int(tx.get('value', '0x0'), 16)
                    value_eth = value_wei / 1e18
                    value_usd = value_eth * eth_price

                    if self._is_whale_transaction(tx, eth_price):
                        tx_type, protocol = self._identify_tx_type(tx)

                        tx_data = {
                            'tx_hash': tx.get('hash', ''),
                            'from_address': tx.get('from', ''),
                            'to_address': tx.get('to', '0x'),
                            'value_eth': value_eth,
                            'value_usd': value_usd,
                            'gas_used': int(tx.get('gas', '0x0'), 16),
                            'gas_price': tx.get('gasPrice'),
                            'tx_type': tx_type,
                            'protocol': protocol,
                            'block_number': block_num,
                            'timestamp': int(block.get('timestamp', time.time())),
                        }

                        tx_id = self.db.insert_eth_tx(tx_data)
                        tx_data['id'] = tx_id
                        whale_txs.append(tx_data)

                        # Update whale wallets
                        self.db.insert_whale_wallet(tx.get('from'), 'eth', value_usd)
                        if tx.get('to'):
                            self.db.insert_whale_wallet(tx.get('to'), 'eth', value_usd)

                        # Generate alert for very large transfers
                        if value_eth >= 100 or value_usd >= 500_000:
                            self.db.insert_whale_alert({
                                'alert_type': 'large_transfer',
                                'chain': 'eth',
                                'address': tx.get('from'),
                                'amount': value_eth,
                                'currency': 'ETH',
                                'description': f'Large transfer: {value_eth:.2f} ETH (${value_usd:,.0f}) via {protocol or tx_type}',
                            })

        print(f"  Found {len(whale_txs)} whale transactions in block scan")
        return whale_txs


if __name__ == '__main__':
    # Test the monitor
    monitor = EthereumWhaleMonitor()

    # Monitor known whale wallets
    print("=== Monitoring Known Whale Wallets ===")
    results = monitor.monitor_whales(lookback_hours=24)

    # Scan recent blocks
    print("\n=== Scanning Recent Blocks ===")
    block_txs = monitor.scan_large_blocks(num_blocks=50)

    print(f"\n=== Summary ===")
    print(f"Wallet transactions: {len(results.get('transactions', []))}")
    print(f"Block scan transactions: {len(block_txs)}")

    # Print stats
    print(f"\n=== Database Stats ===")
    stats = monitor.db.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    monitor.db.close()
