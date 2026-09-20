"""Refresh repository documentation counts directly from source ASTs."""
import ast
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
contract_path = ROOT / "contracts/headroom.py"
contract_source = contract_path.read_text(encoding="utf-8")
tree = ast.parse(contract_source)
counts = {"view": 0, "write": 0}
for node in ast.walk(tree):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        for decorator in node.decorator_list:
            name = ast.unparse(decorator.func if isinstance(decorator, ast.Call) else decorator)
            if name == "gl.public.view":
                counts["view"] += 1
            elif name == "gl.public.write" or name.startswith("gl.public.write."):
                counts["write"] += 1
tests = ast.parse((ROOT / "tests/direct/test_headroom.py").read_text(encoding="utf-8"))
test_count = sum(isinstance(node, ast.FunctionDef) and node.name.startswith("test_") for node in tests.body)
values = {"[[CONTRACT_LINES]]": str(len(contract_source.splitlines())), "[[PUBLIC_VIEWS]]": str(counts["view"]), "[[PUBLIC_WRITES]]": str(counts["write"]), "[[DIRECT_TESTS]]": str(test_count)}
for relative in ("README.md", "docs/REVIEW_EVIDENCE.md", "BUILD_STATUS.md", "VERIFICATION_STATUS.md", "STATIC_VERIFICATION.md"):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    for token, value in values.items():
        text = text.replace(token, value)
    path.write_text(text, encoding="utf-8")
print(f"contract_lines={values['[[CONTRACT_LINES]]']}")
print(f"public_views={values['[[PUBLIC_VIEWS]]']}")
print(f"public_writes={values['[[PUBLIC_WRITES]]']}")
print(f"direct_mode_tests={values['[[DIRECT_TESTS]]']}")
