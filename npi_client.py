"""
NPI Provider Search Client

A self-contained module for searching healthcare providers via the CMS NPI Registry API.
Implements the contract for provider search with taxonomy and postal code filtering.

Basic Usage:
    >>> from npi_client import search_npi_providers
    >>> results = search_npi_providers("massage therapist", "98029")
    >>> print(f"Found {results['result_count']} providers")
"""

from typing import Dict, List, Optional, Any
import requests


# API Configuration
NPI_API_BASE_URL = "https://npiregistry.cms.hhs.gov/api/"
API_VERSION = "2.1"
DEFAULT_TIMEOUT = 30  # seconds


def search_npi_providers(
    taxonomy_description: str,
    postal_code: str,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Search CMS NPI Registry for healthcare providers.

    This is the primary public interface for querying the NPI registry.
    Searches by provider specialty (taxonomy) and postal code.

    Args:
        taxonomy_description: Provider specialty or type (e.g., "massage therapist", "physician")
        postal_code: US postal code to search within (e.g., "98029")
        limit: Maximum number of results to return (default: 20, max: 200)

    Returns:
        Dictionary with search results:
            {
                "result_count": int,  # Total number of providers found
                "providers": List[Dict] with each provider containing:
                    - name: str - Provider's full name or organization name
                    - specialty: str - Primary specialty/taxonomy description
                    - address: str - Formatted location address
                    - phone: str - Contact phone number
                    - license: str - License number (if available, else "N/A")
            }

    Raises:
        ValueError: If API returns an error response
        requests.RequestException: If network request fails

    Examples:
        >>> # Search for massage therapists in a specific area
        >>> results = search_npi_providers("massage therapist", "98029", limit=10)
        >>> print(f"Found {results['result_count']} providers")
        >>> for provider in results['providers']:
        ...     print(f"{provider['name']} - {provider['specialty']}")

        >>> # Handle empty results gracefully
        >>> results = search_npi_providers("unicorn specialist", "00000")
        >>> assert results['result_count'] == 0
        >>> assert results['providers'] == []
    """
    # Build query parameters
    params = {
        "version": API_VERSION,
        "taxonomy_description": taxonomy_description,
        "postal_code": postal_code,
        "limit": limit
    }

    try:
        # Make API request
        response = requests.get(NPI_API_BASE_URL, params=params, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.Timeout:
        raise requests.RequestException(
            f"NPI API request timed out after {DEFAULT_TIMEOUT} seconds. "
            f"Please try again or reduce the limit parameter."
        )
    except requests.exceptions.ConnectionError as e:
        raise requests.RequestException(
            f"Failed to connect to NPI Registry API at {NPI_API_BASE_URL}. "
            f"Please check your internet connection. Error: {str(e)}"
        )
    except requests.exceptions.RequestException as e:
        raise requests.RequestException(
            f"Network error while contacting NPI Registry API: {str(e)}"
        )

    # Check for API errors
    if "Errors" in data and data["Errors"]:
        error_messages = [err.get("description", str(err)) for err in data["Errors"]]
        raise ValueError(
            f"NPI API returned errors: {'; '.join(error_messages)}"
        )

    # Extract results
    results = data.get("results", [])
    result_count = data.get("result_count", 0)

    # Parse provider data
    providers = []
    for result in results:
        provider = {
            "name": _format_provider_name(result),
            "specialty": _get_primary_specialty(result.get("taxonomies", [])),
            "address": _format_address(result.get("addresses", [])),
            "phone": _format_phone(
                _get_location_phone(result.get("addresses", []))
            ),
            "license": _get_license_number(result.get("taxonomies", []))
        }
        providers.append(provider)

    return {
        "result_count": result_count,
        "providers": providers
    }


def _format_provider_name(result: Dict) -> str:
    """
    Extract and format provider name from API result.

    Uses individual name (first + last) for people, or organization name for entities.

    Args:
        result: Single provider result from NPI API

    Returns:
        Formatted provider name, or "N/A" if no name available

    Examples:
        >>> result = {"basic": {"first_name": "John", "last_name": "Doe"}}
        >>> _format_provider_name(result)
        'John Doe'

        >>> result = {"basic": {"organization_name": "ABC Medical Center"}}
        >>> _format_provider_name(result)
        'ABC Medical Center'
    """
    basic = result.get("basic", {})

    # Try individual name first (first_name + last_name)
    first_name = (basic.get("first_name") or "").strip()
    last_name = (basic.get("last_name") or "").strip()

    if first_name and last_name:
        return f"{first_name} {last_name}"
    elif first_name:
        return first_name
    elif last_name:
        return last_name

    # Fall back to organization name
    org_name = (basic.get("organization_name") or "").strip()
    if org_name:
        return org_name

    return "N/A"


def _format_address(addresses: List[Dict]) -> str:
    """
    Extract and format location address from provider addresses.

    Prioritizes addresses with address_purpose="LOCATION", falls back to first address.

    Args:
        addresses: List of address dictionaries from NPI API

    Returns:
        Formatted address string "street, city, state zip", or "N/A" if no address

    Examples:
        >>> addresses = [{
        ...     "address_purpose": "LOCATION",
        ...     "address_1": "123 Main St",
        ...     "city": "Seattle",
        ...     "state": "WA",
        ...     "postal_code": "98029"
        ... }]
        >>> _format_address(addresses)
        '123 Main St, Seattle, WA 98029'
    """
    if not addresses:
        return "N/A"

    # Find location address
    location_addr = None
    for addr in addresses:
        if addr.get("address_purpose") == "LOCATION":
            location_addr = addr
            break

    # Fall back to first address if no location address found
    if not location_addr:
        location_addr = addresses[0]

    # Build address string
    parts = []

    # Street address
    address_1 = (location_addr.get("address_1") or "").strip()
    address_2 = (location_addr.get("address_2") or "").strip()
    if address_1:
        parts.append(address_1)
        if address_2:
            parts[-1] += f" {address_2}"

    # City, State ZIP
    city = (location_addr.get("city") or "").strip()
    state = (location_addr.get("state") or "").strip()
    postal = (location_addr.get("postal_code") or "").strip()

    if city and state and postal:
        parts.append(f"{city}, {state} {postal}")
    elif city and state:
        parts.append(f"{city}, {state}")
    elif city:
        parts.append(city)

    return ", ".join(parts) if parts else "N/A"


def _format_phone(phone: Optional[str]) -> str:
    """
    Format phone number for display.

    Args:
        phone: Raw phone number string (may be None or empty)

    Returns:
        Formatted phone number or "N/A" if not available

    Examples:
        >>> _format_phone("4255551234")
        '425-555-1234'

        >>> _format_phone("425-555-1234")
        '425-555-1234'

        >>> _format_phone(None)
        'N/A'

        >>> _format_phone("")
        'N/A'
    """
    if not phone or not phone.strip():
        return "N/A"

    phone = phone.strip()

    # If already formatted, return as-is
    if "-" in phone or "(" in phone:
        return phone

    # Format 10-digit numbers as XXX-XXX-XXXX
    digits_only = "".join(c for c in phone if c.isdigit())
    if len(digits_only) == 10:
        return f"{digits_only[:3]}-{digits_only[3:6]}-{digits_only[6:]}"

    # Return as-is if not standard format
    return phone


def _get_location_phone(addresses: List[Dict]) -> Optional[str]:
    """
    Extract phone number from location address.

    Args:
        addresses: List of address dictionaries from NPI API

    Returns:
        Phone number string or None if not found
    """
    if not addresses:
        return None

    # Find location address
    for addr in addresses:
        if addr.get("address_purpose") == "LOCATION":
            phone = addr.get("telephone_number")
            if phone:
                return phone

    # Fall back to first address with phone
    for addr in addresses:
        phone = addr.get("telephone_number")
        if phone:
            return phone

    return None


def _get_primary_specialty(taxonomies: List[Dict]) -> str:
    """
    Extract primary specialty/taxonomy description.

    Args:
        taxonomies: List of taxonomy dictionaries from NPI API

    Returns:
        Primary specialty description, or "N/A" if not available

    Examples:
        >>> taxonomies = [
        ...     {"primary": True, "desc": "Massage Therapist"},
        ...     {"primary": False, "desc": "Physical Therapist"}
        ... ]
        >>> _get_primary_specialty(taxonomies)
        'Massage Therapist'
    """
    if not taxonomies:
        return "N/A"

    # Find primary taxonomy
    for taxonomy in taxonomies:
        if taxonomy.get("primary", False):
            desc = (taxonomy.get("desc") or "").strip()
            if desc:
                return desc

    # Fall back to first taxonomy
    if taxonomies:
        desc = (taxonomies[0].get("desc") or "").strip()
        if desc:
            return desc

    return "N/A"


def _get_license_number(taxonomies: List[Dict]) -> str:
    """
    Extract license number from primary taxonomy.

    Args:
        taxonomies: List of taxonomy dictionaries from NPI API

    Returns:
        License number from primary taxonomy, or "N/A" if not available

    Examples:
        >>> taxonomies = [
        ...     {"primary": True, "license": "LIC12345", "state": "WA"},
        ...     {"primary": False, "license": "LIC67890", "state": "OR"}
        ... ]
        >>> _get_license_number(taxonomies)
        'LIC12345 (WA)'
    """
    if not taxonomies:
        return "N/A"

    # Find primary taxonomy
    for taxonomy in taxonomies:
        if taxonomy.get("primary", False):
            license_num = (taxonomy.get("license") or "").strip()
            if license_num:
                state = (taxonomy.get("state") or "").strip()
                if state:
                    return f"{license_num} ({state})"
                return license_num

    # Fall back to first taxonomy with license
    for taxonomy in taxonomies:
        license_num = (taxonomy.get("license") or "").strip()
        if license_num:
            state = (taxonomy.get("state") or "").strip()
            if state:
                return f"{license_num} ({state})"
            return license_num

    return "N/A"
