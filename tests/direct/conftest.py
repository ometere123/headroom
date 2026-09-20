import sys
import pytest
from gltest.direct import create_address

@pytest.fixture(autouse=True)
def direct_mode_clock_warp_tracks_consensus_message(direct_vm):
    """gltest-test 0.29.2 updates sender/value on warp but leaves message_raw.datetime stale."""
    original_warp=direct_vm.warp
    def warp_and_refresh(timestamp):
        original_warp(timestamp)
        gl=sys.modules.get("genlayer.gl")
        message_raw=getattr(gl,"message_raw",None) if gl is not None else None
        if isinstance(message_raw,dict):message_raw["datetime"]=timestamp
    direct_vm.warp=warp_and_refresh
    yield
    direct_vm.warp=original_warp

def hx(value):
    if hasattr(value, "as_hex"):
        return value.as_hex
    return "0x" + value.hex()
