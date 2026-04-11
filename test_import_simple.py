import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("Simple Import Test")
print("=" * 60)

print("\n[1/2] Testing main.py import...")
try:
    from main import SQLAgent
    print("[OK] main.SQLAgent imported")
except Exception as e:
    print(f"[FAIL] main.SQLAgent: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n[2/2] Testing backend.app import...")
try:
    from backend.app import app
    print("[OK] backend.app imported")
except Exception as e:
    print(f"[FAIL] backend.app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("[OK] All imports passed!")
print("=" * 60)
