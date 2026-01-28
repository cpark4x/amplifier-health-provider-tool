#!/usr/bin/env python3
"""Test the tool directly without Amplifier."""

import asyncio
import sys

# Mock the minimal coordinator interface
class MockCoordinator:
    def __init__(self):
        self.mounted_tools = {}
    
    async def mount(self, module_type, tool, name):
        """Mock mount function."""
        self.mounted_tools[name] = tool
        print(f"✓ Registered tool: {name}")

async def test_tool():
    """Test the tool mounting and execution."""
    # Import after adding to path
    sys.path.insert(0, '/Users/chrispark/amplifier-health-provider-tool')
    from amplifier_tool_health_provider import mount
    
    # Create mock coordinator
    coordinator = MockCoordinator()
    
    # Configuration
    config = {
        'healthcare': {
            'primary_insurance': {
                'company': 'premera',
                'plan_name': 'Test Plan'
            },
            'secondary_insurance': {
                'company': 'aetna',
                'plan_name': 'Test Plan'
            },
            'location': {
                'zip_code': '98029',
                'city': 'Issaquah',
                'state': 'WA'
            },
            'preferences': {
                'search_radius_miles': 10
            }
        }
    }
    
    # Mount the tool
    print("Mounting tool...")
    tool = await mount(coordinator, config)
    print(f"✓ Tool mounted: {tool}")
    print(f"✓ Tool name: {tool.name}")
    print(f"✓ Tool description length: {len(tool.description)} chars")
    
    # Test execution
    print("\nTesting tool execution...")
    result = await tool.execute({
        "service_type": "massage therapy",
        "insurance": "primary"
    })
    
    print(f"✓ Execution result: {result}")
    print(f"  Success: {result.success}")
    if result.success:
        print(f"  Output: {result.output}")
    else:
        print(f"  Error: {result.error}")
    
    return result

if __name__ == "__main__":
    result = asyncio.run(test_tool())
    if result.success:
        print("\n✓✓✓ Tool test PASSED! ✓✓✓")
        sys.exit(0)
    else:
        print("\n✗✗✗ Tool test FAILED ✗✗✗")
        sys.exit(1)
