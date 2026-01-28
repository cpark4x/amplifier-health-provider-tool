#!/usr/bin/env python3
"""Quick test to verify bundle can load the tool."""

import sys
sys.path.insert(0, '/Users/chrispark/amplifier-health-provider-tool')

from amplifier_tool_health_provider import mount

# Simulate a basic coordinator
class MockCoordinator:
    pass

config = {
    "healthcare": {
        "primary_insurance": {"company": "premera"},
        "location": {"zip_code": "98101"}
    }
}

try:
    result = mount(MockCoordinator(), config)
    print("✓ Tool mount successful!")
    print(f"✓ Tool registered: {list(result.keys())}")
    print("✓ Tool has description:", "description" in result["health_provider_search"])
    print("\n✓✓✓ Tool is ready to use! ✓✓✓")
except Exception as e:
    print(f"✗ Error mounting tool: {e}")
    import traceback
    traceback.print_exc()
