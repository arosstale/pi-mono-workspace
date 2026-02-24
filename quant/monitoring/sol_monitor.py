"""
Solana whale monitor using public RPC APIs
"""

import requests
import time
import struct
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from database import WhaleDatabase
import base58

# Solana public RPC endpoints (free)
RPC_ENDPOINTS = [
    'https://api.mainnet-beta.solana.com',
    'https://solana-api.projectserum.com',
    'https://rpc.ankr.com/solana',
]

# Known Solana DEX and program addresses
DEX_PROGRAMS = {
    'jupiter': 'JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4',
    'raydium': '675kPX9MHTjS2zt1qf5Wk6vR5Jc6jwNfSaW2aRGwhp',
    'orca': '9W959DqEETiGZocYGBQMYVMTVJgfJHPA3qbWxnFvXsBJ',
    'serum': '9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin',
}

# System program for transfers
SYSTEM_PROGRAM = '11111111111111111111111111111111'

# Known whale wallets (starting seed list)
INITIAL_WHALES_SOL = [
    '7RCz8Z1QDgkzF7yVz5pC2B9p8G3qL4wX6Y9nN1vM2PjK',
    '5vD9Q1x8mP3L7nT2kY4rG6wZ5vN8c1xM3L7pT2kY9nR',
]

class SolanaWhaleMonitor:
    """Monitor Solana whale transactions using public RPC"""

    def __init__(self, rpc_url: Optional[str] = None):
        self.rpc_url = rpc_url or RPC_ENDPOINTS[0]
        self.db = WhaleDatabase()
        self.min_sol_threshold = 1000.0  # Minimum SOL to track
        self.min_usd_threshold = 50_000  # Minimum USD value to track
        self.rpc_index = 0

    def _make_rpc_request(self, method: str, params: list = None) -> Optional[Any]:
        """Make RPC request with failover"""
        if params is None:
            params = []

        payload = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': method,
            'params': params,
        }

        # Try each endpoint
        for i, url in enumerate(RPC_ENDPOINTS):
            try:
                response = requests.post(url, json=payload, timeout=30)
                response.raise_for_status()
                data = response.json()

                if 'error' in data:
                    print(f"RPC Error from {url}: {data['error']}")
                    continue

                return data.get('result')
            except Exception as e:
                print(f"RPC request failed to {url}: {e}")
                continue

        return None

    def get_sol_price(self) -> float:
        """Get SOL price via CoinGecko (free, no API key)"""
        try:
            response = requests.get(
                'https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd',
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return float(data.get('solana', {}).get('usd', 0))
        except Exception as e:
            print(f"Failed to get SOL price: {e}")
            return 0

    def get_latest_slot(self) -> Optional[int]:
        """Get latest slot number"""
        return self._make_rpc_request('getSlot')

    def get_signatures_for_address(self, address: str, limit: int = 1000) -> List[Dict[str, Any]]:
        """Get transaction signatures for an address"""
        result = self._make_rpc_request(
            'getSignaturesForAddress',
            [address, {'limit': limit}]
        )
        if result:
            return result
        return []

    def get_transaction(self, signature: str) -> Optional[Dict[str, Any]]:
        """Get transaction details"""
        result = self._make_rpc_request(
            'getTransaction',
            [signature, {'encoding': 'jsonParsed', 'maxSupportedTransactionVersion': 0}]
        )
        if result:
            return result
        return None

    def _parse_transfer_amount(self, instruction: Any) -> tuple[float, str, str]:
        """Parse transfer instruction to get amount, from, to"""
        try:
            # Handle different instruction formats
            if isinstance(instruction, str):
                return 0, '', ''

            # Ensure we have a dict
            if not isinstance(instruction, dict):
                return 0, '', ''

            program_id = instruction.get('programId', '')
            parsed = instruction.get('parsed', {})

            if not isinstance(parsed, dict):
                return 0, '', ''

            info = parsed.get('info', {})

            if not isinstance(info, dict):
                return 0, '', ''

            tx_type = parsed.get('type', '').lower() if isinstance(parsed.get('type'), str) else ''

            if 'transfer' in tx_type:
                # System program transfer
                amount = float(info.get('lamports', 0)) / 1e9  # Convert lamports to SOL
                return amount, info.get('source', ''), info.get('destination', '')

            elif 'transferchecked' in tx_type:
                # SPL token transfer
                token_amount = info.get('tokenAmount', {})
                if isinstance(token_amount, dict):
                    amount = float(token_amount.get('amount', 0))
                    decimals = token_amount.get('decimals', 0)
                    amount = amount / (10 ** decimals)
                else:
                    amount = 0
                return amount, info.get('source', ''), info.get('destination', '')

        except Exception as e:
            # Silently skip parsing errors
            pass

        return 0, '', ''

    def _identify_protocol(self, program_ids: List[str]) -> Optional[str]:
        """Identify DEX protocol from program IDs"""
        for program_id in program_ids:
            for protocol, addr in DEX_PROGRAMS.items():
                if program_id == addr:
                    return protocol
        return None

    def _classify_transaction(self, tx: Dict[str, Any]) -> tuple[str, Optional[str]]:
        """Classify transaction type and protocol"""
        meta = tx.get('meta', {}) or {}
        message = tx.get('transaction', {}).get('message', {}) or {}

        if not message:
            return 'unknown', None

        # Get all program IDs
        instructions = message.get('instructions', []) or []
        account_keys = message.get('accountKeys', []) or []

        # Extract program IDs from account keys
        program_ids = []
        if isinstance(account_keys, list):
            for acc in account_keys:
                if isinstance(acc, dict) and acc.get('writable'):
                    program_ids.append(acc)

        # Check for DEX protocols
        protocol = self._identify_protocol(program_ids)

        if protocol:
            return 'swap', protocol

        # Check for contract interaction
        if len(instructions) > 1:
            inner_instructions = meta.get('innerInstructions', []) or []
            if inner_instructions:
                return 'program', None
            return 'contract', None

        # Simple transfer
        if len(instructions) == 1:
            return 'transfer', None

        return 'contract', None

    def _is_whale_transaction(self, amount_sol: float, sol_price: float) -> bool:
        """Check if transaction meets whale criteria"""
        amount_usd = amount_sol * sol_price
        return amount_sol >= self.min_sol_threshold or amount_usd >= self.min_usd_threshold

    def monitor_wallet(self, address: str, limit: int = 1000) -> List[Dict[str, Any]]:
        """Monitor a single wallet for whale transactions"""
        print(f"Monitoring SOL wallet: {address}")

        sol_price = self.get_sol_price()
        if not sol_price:
            print("Could not get SOL price, using $0")
            sol_price = 0

        signatures = self.get_signatures_for_address(address, limit=limit)
        whale_txs = []

        for sig_info in signatures:
            signature = sig_info.get('signature')
            if not signature:
                continue

            tx = self.get_transaction(signature)
            if not tx or not tx.get('meta'):
                continue

            meta = tx['meta']
            message = tx.get('transaction', {}).get('message', {})
            instructions = message.get('instructions', [])

            total_amount = 0
            from_addr = address
            to_addr = None

            # Parse all instructions to find transfers
            for instr in instructions:
                amount, src, dst = self._parse_transfer_amount(instr)
                if amount > 0:
                    total_amount += amount
                    if src and (not from_addr or src.lower() == address.lower()):
                        from_addr = src
                    if dst:
                        to_addr = dst

            # Check if this is a whale transaction
            if total_amount > 0 and self._is_whale_transaction(total_amount, sol_price):
                tx_type, protocol = self._classify_transaction(tx)

                # Get fee
                fee = meta.get('fee', 0)

                tx_data = {
                    'tx_sig': signature,
                    'from_address': from_addr,
                    'to_address': to_addr or address,
                    'amount_sol': total_amount,
                    'amount_usd': total_amount * sol_price,
                    'fee_lamports': fee,
                    'tx_type': tx_type,
                    'protocol': protocol,
                    'slot': tx.get('slot'),
                    'timestamp': int(tx.get('blockTime', time.time())),
                }

                # Store in database
                tx_id = self.db.insert_sol_tx(tx_data)
                tx_data['id'] = tx_id
                whale_txs.append(tx_data)

                # Update whale wallet record
                self.db.insert_whale_wallet(from_addr, 'sol', total_amount * sol_price)
                if to_addr:
                    self.db.insert_whale_wallet(to_addr, 'sol', total_amount * sol_price)

                # Generate alert for very large transfers
                if total_amount >= 10000 or (total_amount * sol_price) >= 500_000:
                    self.db.insert_whale_alert({
                        'alert_type': 'large_transfer',
                        'chain': 'sol',
                        'address': from_addr,
                        'amount': total_amount,
                        'currency': 'SOL',
                        'description': f'Large transfer: {total_amount:.2f} SOL (${total_amount * sol_price:,.0f}) via {protocol or tx_type}',
                    })

            # Rate limiting
            time.sleep(0.1)

        print(f"  Found {len(whale_txs)} whale transactions")
        return whale_txs

    def monitor_whales(self, addresses: List[str] = None, limit: int = 500) -> Dict[str, Any]:
        """Monitor multiple whale wallets"""
        addresses = addresses or INITIAL_WHALES_SOL
        all_whale_txs = []

        print(f"Monitoring {len(addresses)} SOL wallets")

        for address in addresses:
            whale_txs = self.monitor_wallet(address, limit=limit)
            all_whale_txs.extend(whale_txs)
            time.sleep(0.5)  # Be nice to RPCs

        return {
            'wallets_monitored': len(addresses),
            'whale_transactions': len(all_whale_txs),
            'transactions': all_whale_txs,
        }

    def scan_recent_blocks(self, num_blocks: int = 100) -> List[Dict[str, Any]]:
        """Scan recent blocks for large transactions"""
        sol_price = self.get_sol_price()
        if not sol_price:
            sol_price = 0

        latest_slot = self.get_latest_slot()
        if not latest_slot:
            print("Could not get latest slot")
            return []

        whale_txs = []
        print(f"Scanning last {num_blocks} slots for large transactions")

        # Scan blocks in batches
        start_slot = latest_slot
        for i in range(num_blocks):
            slot = start_slot - i

            # Get block
            result = self._make_rpc_request(
                'getBlock',
                [slot, {'encoding': 'jsonParsed', 'maxSupportedTransactionVersion': 0, 'transactionsDetails': 'full'}]
            )

            if not result:
                continue

            block = result
            transactions = block.get('transactions', [])

            for tx in transactions:
                meta = tx.get('meta', {})
                message = tx.get('transaction', {}).get('message', {})

                if not message:
                    continue

                instructions = message.get('instructions', [])
                total_amount = 0
                from_addr = None
                to_addr = None

                # Parse transfers
                for instr in instructions:
                    amount, src, dst = self._parse_transfer_amount(instr)
                    if amount > 0:
                        total_amount += amount
                        if not from_addr:
                            from_addr = src
                        if dst:
                            to_addr = dst

                # Check whale criteria
                if total_amount > 0 and self._is_whale_transaction(total_amount, sol_price):
                    tx_type, protocol = self._classify_transaction(tx)
                    fee = meta.get('fee', 0)
                    signature = tx.get('transaction', {}).get('signatures', [''])[0]

                    tx_data = {
                        'tx_sig': signature,
                        'from_address': from_addr or 'unknown',
                        'to_address': to_addr or 'unknown',
                        'amount_sol': total_amount,
                        'amount_usd': total_amount * sol_price,
                        'fee_lamports': fee,
                        'tx_type': tx_type,
                        'protocol': protocol,
                        'slot': slot,
                        'timestamp': int(block.get('blockTime', time.time())),
                    }

                    tx_id = self.db.insert_sol_tx(tx_data)
                    tx_data['id'] = tx_id
                    whale_txs.append(tx_data)

                    # Update whale wallets
                    if from_addr:
                        self.db.insert_whale_wallet(from_addr, 'sol', total_amount * sol_price)
                    if to_addr:
                        self.db.insert_whale_wallet(to_addr, 'sol', total_amount * sol_price)

            time.sleep(0.05)  # Rate limiting

        print(f"  Found {len(whale_txs)} whale transactions in block scan")
        return whale_txs


if __name__ == '__main__':
    # Test the monitor
    monitor = SolanaWhaleMonitor()

    # Monitor known whale wallets
    print("=== Monitoring Known Whale Wallets ===")
    results = monitor.monitor_whales(limit=200)

    # Scan recent blocks
    print("\n=== Scanning Recent Slots ===")
    block_txs = monitor.scan_recent_blocks(num_blocks=100)

    print(f"\n=== Summary ===")
    print(f"Wallet transactions: {len(results.get('transactions', []))}")
    print(f"Block scan transactions: {len(block_txs)}")

    # Print stats
    print(f"\n=== Database Stats ===")
    stats = monitor.db.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    monitor.db.close()
