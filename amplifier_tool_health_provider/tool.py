"""Health Insurance Provider Search Tool."""

import webbrowser
from typing import Any
from urllib.parse import urlencode

from amplifier_core.coordinator import ModuleCoordinator
from amplifier_core.models import ToolResult


class HealthProviderTool:
    """AI-driven health insurance provider search tool.
    
    Opens insurance provider directories with pre-filled search parameters
    based on user's stored insurance and location information.
    """

    def __init__(self, config: dict[str, Any]):
        """Initialize the health provider search tool.
        
        Args:
            config: Configuration including user's healthcare info
        """
        self.config = config
        self.healthcare_config = config.get("healthcare", {})

    @property
    def name(self) -> str:
        """Tool name for invocation."""
        return "health_provider_search"

    @property
    def description(self) -> str:
        """Human-readable tool description."""
        return (
            "Search for healthcare providers (doctors, specialists, therapists, optical shops, etc.) "
            "that accept the user's health insurance. Opens the insurance company's provider directory "
            "with pre-filled search parameters based on stored user information.\n\n"
            "Parameters:\n"
            "- service_type (str, required): Type of healthcare service needed. "
            "Examples: 'massage therapy', 'contact lenses', 'optometrist', 'physical therapy', "
            "'acupuncture', 'chiropractor', 'primary care', 'dermatology', etc.\n"
            "- insurance (str, optional): Which insurance to search with. Options: 'primary', 'secondary', 'both'. "
            "Defaults to 'primary'\n"
            "- radius_miles (int, optional): Search radius in miles. Uses user's preference if not specified.\n"
            "- location_override (str, optional): Override user's stored location with a specific zip code or city"
        )

    async def execute(self, input: dict[str, Any]) -> ToolResult:
        """Execute the provider search.
        
        Args:
            input: Tool input parameters
            
        Returns:
            ToolResult with search results
        """
        try:
            # Extract parameters
            service_type = input.get("service_type")
            if not service_type:
                return ToolResult(
                    success=False,
                    error={"message": "service_type parameter is required"}
                )

            insurance = input.get("insurance", "primary")
            radius_miles = input.get("radius_miles")
            location_override = input.get("location_override")

            # Get location
            location = location_override or self._get_location()
            if not location:
                return ToolResult(
                    success=False,
                    error={"message": "No location configured. Please set your zip code in healthcare config."}
                )

            # Get search radius
            radius = radius_miles or self.healthcare_config.get("preferences", {}).get("search_radius_miles", 10)

            # Determine which insurance(s) to search
            insurances_to_search = []
            if insurance in ["primary", "both"]:
                primary = self.healthcare_config.get("primary_insurance")
                if primary:
                    insurances_to_search.append(("primary", primary))

            if insurance in ["secondary", "both"]:
                secondary = self.healthcare_config.get("secondary_insurance")
                if secondary:
                    insurances_to_search.append(("secondary", secondary))

            if not insurances_to_search:
                return ToolResult(
                    success=False,
                    error={"message": f"No {insurance} insurance configured. Please set up your insurance information."}
                )

            # Open search for each insurance
            results = []
            for insurance_type, insurance_config in insurances_to_search:
                company = insurance_config.get("company", "").lower()
                
                if company == "premera":
                    url = self._build_premera_url(service_type, location, radius)
                elif company == "aetna":
                    url = self._build_aetna_url(service_type, location, radius)
                else:
                    results.append({
                        "insurance": insurance_type,
                        "company": company,
                        "error": f"Unsupported insurance company: {company}",
                    })
                    continue

                # Open in browser
                try:
                    webbrowser.open(url)
                    results.append({
                        "insurance": insurance_type,
                        "company": company,
                        "url": url,
                        "opened": True,
                    })
                except Exception as e:
                    results.append({
                        "insurance": insurance_type,
                        "company": company,
                        "url": url,
                        "opened": False,
                        "error": str(e),
                    })

            # Build helpful message
            specialty = self._map_service_to_specialty(service_type)
            message = (
                f"Opened insurance provider search page(s) in your browser.\n\n"
                f"**What you need to do:**\n"
                f"1. Look for the search form on the insurance website\n"
                f"2. Enter your location: {location}\n"
                f"3. Search for: {specialty}\n"
                f"4. Set radius: {radius} miles\n\n"
                f"**Note:** Insurance websites use JavaScript applications that don't support "
                f"pre-filled search parameters, so you'll need to manually enter these criteria."
            )
            
            return ToolResult(
                success=True,
                output={
                    "service_type": service_type,
                    "specialty": specialty,
                    "location": location,
                    "radius_miles": radius,
                    "results": results,
                    "message": message,
                }
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error={"message": str(e), "type": type(e).__name__}
            )

    def _get_location(self) -> str | None:
        """Get user's location from config."""
        location_config = self.healthcare_config.get("location", {})
        return location_config.get("zip_code") or location_config.get("city")

    def _build_premera_url(self, service_type: str, location: str, radius: int) -> str:
        """Build Premera provider search URL.
        
        Note: Premera uses a JavaScript SPA that doesn't support URL parameter deep-linking.
        Opens to the base search page where users must manually enter criteria.
        
        Args:
            service_type: Type of service (unused - kept for consistency)
            location: Zip code or city (unused - kept for consistency)
            radius: Search radius in miles (unused - kept for consistency)
            
        Returns:
            Premera search URL
        """
        return "https://www.premera.com/wa/visitor/find-a-doctor/"

    def _build_aetna_url(self, service_type: str, location: str, radius: int) -> str:
        """Build Aetna provider search URL.
        
        Note: Aetna also uses a JavaScript SPA without parameter support.
        Opens to their provider search landing page.
        
        Args:
            service_type: Type of service (unused - kept for consistency)
            location: Zip code or city (unused - kept for consistency)
            radius: Search radius in miles (unused - kept for consistency)
            
        Returns:
            Aetna search URL
        """
        return "https://www.aetna.com/individuals-families/find-a-doctor.html"

    def _map_service_to_specialty(self, service_type: str) -> str:
        """Map natural language service type to insurance specialty code.
        
        Args:
            service_type: Natural language description
            
        Returns:
            Specialty string for insurance search
        """
        service_lower = service_type.lower()
        
        # Common mappings
        mappings = {
            "massage": "Massage Therapy",
            "contact lens": "Optometry",
            "contacts": "Optometry",
            "eye doctor": "Optometry",
            "optometrist": "Optometry",
            "glasses": "Optometry",
            "vision": "Optometry",
            "physical therapy": "Physical Therapy",
            "pt": "Physical Therapy",
            "acupuncture": "Acupuncture",
            "chiropractor": "Chiropractic",
            "chiro": "Chiropractic",
            "primary care": "Primary Care",
            "pcp": "Primary Care",
            "dermatology": "Dermatology",
            "skin doctor": "Dermatology",
            "mental health": "Mental Health",
            "therapist": "Mental Health",
            "psychiatrist": "Psychiatry",
            "counselor": "Mental Health",
            "dental": "Dentistry",
            "dentist": "Dentistry",
        }
        
        # Find best match
        for key, specialty in mappings.items():
            if key in service_lower:
                return specialty
        
        # Default: return the service type as-is
        return service_type.title()

    def get_schema(self) -> dict:
        """Return JSON schema for tool input validation."""
        return {
            "type": "object",
            "properties": {
                "service_type": {
                    "type": "string",
                    "description": (
                        "Type of healthcare service needed. Examples: 'massage therapy', 'contact lenses', "
                        "'optometrist', 'physical therapy', 'acupuncture', 'chiropractor', 'primary care', "
                        "'dermatology', etc."
                    ),
                },
                "insurance": {
                    "type": "string",
                    "enum": ["primary", "secondary", "both"],
                    "description": "Which insurance to search with. Defaults to 'primary'",
                    "default": "primary",
                },
                "radius_miles": {
                    "type": "integer",
                    "description": "Search radius in miles. Uses user's preference if not specified.",
                },
                "location_override": {
                    "type": "string",
                    "description": "Override user's stored location with a specific zip code or city",
                },
            },
            "required": ["service_type"],
        }


async def mount(coordinator: ModuleCoordinator, config: dict[str, Any]):
    """Mount the health provider tool.
    
    Args:
        coordinator: Amplifier coordinator instance
        config: Tool configuration
        
    Returns:
        The tool instance
    """
    # Create tool instance
    tool = HealthProviderTool(config=config)
    
    # Register with coordinator
    await coordinator.mount("tools", tool, name="health_provider_search")
    
    # Return the tool instance
    return tool
