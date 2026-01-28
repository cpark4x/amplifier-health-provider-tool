"""Health Insurance Provider Search Tool for Amplifier."""

from amplifier_tool_health_provider.tool import HealthProviderTool

__version__ = "0.1.0"

# Export the mount function for Amplifier
mount = HealthProviderTool.mount

__all__ = ["mount", "HealthProviderTool"]
