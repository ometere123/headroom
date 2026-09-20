# Reproducing Direct Mode

Verified in clean WSL Ubuntu with Python 3.12.3 and an isolated venv at `/home/papito/headroom-stable-venv`. The environment was created without system packages, then installed only from repository `requirements.txt`. The harness used system pip's `--python <venv-python>` option to install into the isolated venv.

```sh
python3 -m venv --without-pip .venv
python3 -m pip --python .venv/bin/python install -r requirements.txt
.venv/bin/python -m pytest tests/direct/ -q --tb=short
python3 -m pip --python .venv/bin/python freeze
```

Resolved top-level versions: `genlayer-test==0.29.2`, `genlayer-py==0.16.3`, `genvm-linter==0.11.1rc2`, `pytest==9.0.2`. The GenLayer package pair is compatible: genlayer-test 0.29.2 declares `genlayer-py>=0.13,<0.17`; 0.16.3 satisfies it. The complete environment freeze appears below.

The contract header pins runner `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`. Direct Mode uses the official GenVM `v0.2.16` universal archive in genlayer-test’s cache; the workflow fetches that version explicitly because genlayer-test 0.29.2 otherwise discovers a latest tag whose asset currently returns 404. The exact archive exists and contains the pinned runner (validated by the passing suite).

Direct Mode result: **54 passed**. `tests/direct/conftest.py` includes a focused harness compatibility shim: genlayer-test 0.29.2's `vm.warp` moves its VM clock but leaves the cached message timestamp unchanged, so the fixture synchronizes `gl.message_raw.datetime` after a test warp. Production contract time remains the consensus message timestamp.

```text
aiohappyeyeballs==2.7.1
aiohttp==3.14.3
aiosignal==1.4.0
annotated-types==0.8.0
attrs==26.1.0
bitarray==3.11.0
certifi==2026.7.22
charset-normalizer==3.5.1
ckzg==2.1.8
click==8.5.0
colorama==0.4.0
cytoolz==1.1.0
eth-account==0.14.0
eth-hash==0.8.0
eth-keyfile==0.10.0
eth-keys==0.8.0
eth-rlp==3.0.0
eth-typing==6.0.0
eth-utils==6.0.0
eth_abi==6.0.0
frozenlist==1.8.0
genlayer-py==0.16.3
genlayer-test==0.29.2
genvm-linter==0.11.1rc2
hexbytes==2.0.0
idna==3.20
iniconfig==2.3.0
multidict==6.9.0
nodeenv==1.10.0
numpy==2.5.3
packaging==26.3
parsimonious==0.10.0
pluggy==1.6.0
propcache==0.5.4
py-ecc==8.0.0
pycryptodome==3.23.0
pydantic==2.13.5
pydantic_core==2.46.5
Pygments==2.21.0
pyright==1.1.414
pytest==9.0.2
python-dotenv==1.2.3
pyunormalize==17.0.0
PyYAML==6.0.3
regex==2026.9.10
requests==2.34.2
rlp==5.0.0
toolz==1.1.0
typing-inspection==0.4.4
typing_extensions==4.16.0
urllib3==2.8.0
web3==8.0.0
websockets==17.1
yarl==1.25.1
```
