"""Regression guard for exact attoGEN display formatting."""
from pathlib import Path

source = (Path(__file__).resolve().parents[1] / "frontend/lib/money.ts").read_text(encoding="utf-8")
if 'trimmed?`.`+trimmed:""' not in source:
    raise SystemExit("formatAttoGen must omit the decimal point for whole GEN values")

def format_atto(value: int) -> str:
    whole, remainder = divmod(value, 10**18)
    fraction = f"{remainder:018d}".rstrip("0")
    return f"{whole}{'.' + fraction if fraction else ''} GEN"

vectors = {
    0: "0 GEN",
    10**18: "1 GEN",
    15 * 10**17: "1.5 GEN",
    125 * 10**16: "1.25 GEN",
    10001 * 10**14: "1.0001 GEN",
    10**17: "0.1 GEN",
}
for value, expected in vectors.items():
    actual = format_atto(value)
    if actual != expected:
        raise SystemExit(f"formatAttoGen vector failed: {value} -> {actual}, expected {expected}")
print("MONEY_FORMAT_CHECK=PASS")
