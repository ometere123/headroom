"""Read-only Studionet receipt probe. Set HEADROOM_PROBE_LIVE=1 to query."""
import json, os, urllib.error, urllib.request

TXS = {
    "create": "0xa0792d197bb882b55fffc1198043854a03793c0884c75c51a2563c664c003cbc",
    "close": "0x1898d9f453d82c70cb8194b698bd385d522f9d3f346f089337ee973ddbc5ad20",
    "withdraw": "0xbd1dbd26c544ed3bf542b602bce8a6249af539e877b185dd431a8b7dee9ae99b",
}
if os.environ.get("HEADROOM_PROBE_LIVE") != "1":
    print("READ_ONLY_PROBE=GUARDED; set HEADROOM_PROBE_LIVE=1 to query Studionet")
    raise SystemExit(0)
def call(method, params):
    body=json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":params}).encode()
    request = urllib.request.Request("https://studio.genlayer.com/api", data=body, headers={"Content-Type":"application/json", "User-Agent":"headroom-read-only-probe/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as error:
        try:
            return {"http_error": error.code, "body": error.read().decode("utf-8", "replace")}
        except Exception:
            return {"http_error": error.code}
    except (urllib.error.URLError, TimeoutError) as error:
        return {"transport_error": str(error)}
for name, tx in TXS.items():
    print(name, json.dumps({"receipt":call("gen_getTransactionReceipt", [{"txId":tx}]), "status":call("gen_getTransactionStatus", [tx])}))
