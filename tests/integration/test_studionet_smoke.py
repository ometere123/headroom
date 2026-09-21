"""Opt-in live Studionet smoke test for the canonical deployed contract.

Run after deployment with HEADROOM_CONTRACT=0x...:
    gltest tests/integration/ -v -s --network studionet

The test intentionally skips before deployment instead of pretending that a local
configuration assertion proves network integration.
"""

import os
import rlp
import requests
from eth_utils import to_hex
from genlayer_py.abi.calldata import encode, decode

import pytest

EXPECTED_RPC = "https://studio.genlayer.com/api"
EXPECTED_CHAIN_ID = 61999


@pytest.mark.integration
def test_canonical_deployment_reports_studionet_and_balanced_accounting():
    address = os.getenv("HEADROOM_CONTRACT", "").strip()
    if not address:
        pytest.skip("set HEADROOM_CONTRACT to the finalized Studionet deployment address")

    # genlayer-py 0.16.3 blocks unsigned views before RPC. Issue the same
    # read-only gen_call request directly, with the zero address used by
    # genlayer-js 1.1.8 when no wallet account is connected.
    calldata = encode({"method": "get_stats"})
    serialized = to_hex(rlp.encode([calldata, b"\x00"]))
    response = requests.post(
        EXPECTED_RPC,
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "gen_call",
            "params": [{
                "type": "read",
                "to": address,
                "from": "0x0000000000000000000000000000000000000000",
                "data": serialized,
                "transaction_hash_variant": "latest-final",
            }],
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    assert "error" not in payload, payload.get("error")
    stats = decode(bytes.fromhex(payload["result"].removeprefix("0x")))

    assert stats["network"] == "Studionet"
    assert stats["chain_id"] == str(EXPECTED_CHAIN_ID)
    assert stats["rpc"] == EXPECTED_RPC
    assert stats["accounting_balanced"] is True
    assert stats["admin_controls"] is False
