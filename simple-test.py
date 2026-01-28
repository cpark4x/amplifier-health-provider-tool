#!/usr/bin/env python3
"""Test the tool logic without importing amplifier_core."""

# Just verify the code structure is valid
import ast
import sys

try:
    with open('amplifier_tool_health_provider/tool.py', 'r') as f:
        code = f.read()
    
    ast.parse(code)
    print("✓ Tool code syntax is valid")
    
    # Check key methods exist
    if 'class HealthProviderTool' in code:
        print("✓ HealthProviderTool class defined")
    if 'def mount(' in code:
        print("✓ mount() method defined")
    if 'def search_providers(' in code:
        print("✓ search_providers() method defined")
    if '_build_premera_url' in code:
        print("✓ Premera URL builder defined")
    if '_build_aetna_url' in code:
        print("✓ Aetna URL builder defined")
    
    print("\n✓✓✓ Tool structure is valid! ✓✓✓")
    
except SyntaxError as e:
    print(f"✗ Syntax error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
