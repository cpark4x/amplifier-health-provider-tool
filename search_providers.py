#!/usr/bin/env python3
"""Standalone health provider search script.

Run this directly to test the provider search functionality:
    python3 search_providers.py "massage therapy"
    python3 search_providers.py "contact lenses" --insurance secondary
"""

import argparse
import webbrowser
from urllib.parse import urlencode

from npi_client import search_npi_providers


# Configuration (matches your settings.yaml)
CONFIG = {
    "primary_insurance": {
        "company": "premera",
        "plan_name": "Your Premera Plan"
    },
    "secondary_insurance": {
        "company": "aetna",
        "plan_name": "Your Aetna Plan"
    },
    "location": {
        "zip_code": "98029",
        "city": "Issaquah",
        "state": "WA"
    },
    "search_radius_miles": 10
}


def map_service_to_specialty(service_type: str) -> str:
    """Map natural language to specialty."""
    service_lower = service_type.lower()
    
    mappings = {
        "massage": "massage therapist",
        "contact lens": "optometrist",
        "contacts": "optometrist",
        "eye doctor": "optometrist",
        "optometrist": "optometrist",
        "glasses": "optometrist",
        "vision": "optometrist",
        "physical therapy": "physical therapist",
        "pt": "physical therapist",
        "acupuncture": "acupuncturist",
        "chiropractor": "chiropractor",
        "chiro": "chiropractor",
        "primary care": "primary care",
        "pcp": "primary care",
        "dermatology": "dermatology",
        "skin doctor": "dermatology",
        "mental health": "mental health",
        "therapist": "mental health",
        "psychiatrist": "psychiatry",
        "counselor": "mental health",
        "dental": "dentistry",
        "dentist": "dentistry",
    }
    
    for key, specialty in mappings.items():
        if key in service_lower:
            return specialty
    
    return service_type.lower()


def build_premera_url(service_type: str, location: str, radius: int) -> str:
    """Build Premera provider search URL.
    
    Note: Premera uses a JavaScript SPA that doesn't support URL parameter deep-linking.
    Opens to the base search page where users must manually enter criteria.
    """
    return "https://www.premera.com/wa/visitor/find-a-doctor/"


def build_aetna_url(service_type: str, location: str, radius: int) -> str:
    """Build Aetna provider search URL.
    
    Note: Aetna also uses a JavaScript SPA without parameter support.
    Opens to their provider search landing page.
    """
    return "https://www.aetna.com/individuals-families/find-a-doctor.html"


def search_npi(service_type: str, location: str, limit: int):
    """Search NPI registry and display results."""
    taxonomy = map_service_to_specialty(service_type)
    
    print(f"\n🔍 Searching CMS NPI Registry...")
    print(f"📋 Specialty: {taxonomy}")
    print(f"📍 Location: {location}")
    print(f"🎯 Limit: {limit}\n")
    
    try:
        results = search_npi_providers(taxonomy, location, limit)
        
        if results["result_count"] == 0:
            print("❌ No providers found.")
            print("💡 Try a different specialty or location.\n")
            return
        
        print(f"✅ Found {results['result_count']} provider(s)\n")
        print("="*80)
        
        for i, provider in enumerate(results["providers"], 1):
            print(f"\n{i}. {provider['name']}")
            print(f"   Specialty: {provider['specialty']}")
            print(f"   Address: {provider['address']}")
            print(f"   Phone: {provider['phone']}")
            if provider.get('license') and provider['license'] != 'N/A':
                print(f"   License: {provider['license']}")
        
        print("\n" + "="*80)
        print("\n⚠️  IMPORTANT: Insurance Verification Required")
        print("   The NPI Registry does NOT include insurance information.")
        print("   You must CALL each provider to verify they accept:")
        print(f"   - {CONFIG['primary_insurance']['company'].title()} ({CONFIG['primary_insurance']['plan_name']})")
        print(f"   - {CONFIG['secondary_insurance']['company'].title()} ({CONFIG['secondary_insurance']['plan_name']})")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}\n")


def search_providers(service_type: str, insurance: str = "primary"):
    """Search for healthcare providers."""
    location = CONFIG["location"]["zip_code"]
    radius = CONFIG["search_radius_miles"]
    specialty = map_service_to_specialty(service_type)
    
    print(f"\n🔍 Searching for: {service_type} ({specialty})")
    print(f"📍 Location: {location} ({CONFIG['location']['city']}, {CONFIG['location']['state']})")
    print(f"📏 Radius: {radius} miles")
    print(f"🏥 Insurance: {insurance}\n")
    print("ℹ️  Note: Insurance sites don't support URL parameters.")
    print("   You'll need to manually enter search criteria on the website.\n")
    
    insurances_to_search = []
    if insurance in ["primary", "both"]:
        insurances_to_search.append(("primary", CONFIG["primary_insurance"]))
    if insurance in ["secondary", "both"]:
        insurances_to_search.append(("secondary", CONFIG["secondary_insurance"]))
    
    for insurance_type, insurance_config in insurances_to_search:
        company = insurance_config["company"]
        
        if company == "premera":
            url = build_premera_url(service_type, location, radius)
        elif company == "aetna":
            url = build_aetna_url(service_type, location, radius)
        else:
            print(f"❌ Unsupported insurance: {company}")
            continue
        
        print(f"✅ Opening {company.title()} ({insurance_type} insurance)")
        print(f"   URL: {url}\n")
        
        try:
            webbrowser.open(url)
            print(f"   ✓ Browser opened successfully!\n")
        except Exception as e:
            print(f"   ✗ Failed to open browser: {e}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Search for healthcare providers that accept your insurance"
    )
    parser.add_argument(
        "service_type",
        help="Type of provider (e.g., 'massage therapy', 'contact lenses', 'physical therapy')"
    )
    parser.add_argument(
        "--insurance",
        choices=["primary", "secondary", "both"],
        default="primary",
        help="Which insurance to search (default: primary)"
    )
    parser.add_argument(
        "--mode",
        choices=["npi", "insurance", "both"],
        default="npi",
        help="Search mode (default: npi)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Max providers to return (npi mode, default: 20)"
    )
    
    args = parser.parse_args()
    
    if args.mode == "npi":
        search_npi(args.service_type, CONFIG["location"]["zip_code"], args.limit)
    elif args.mode == "insurance":
        search_providers(args.service_type, args.insurance)
    elif args.mode == "both":
        search_npi(args.service_type, CONFIG["location"]["zip_code"], args.limit)
        print("\n" + "="*80)
        print("Opening insurance websites for verification...\n")
        search_providers(args.service_type, args.insurance)
    
    if args.mode in ["insurance", "both"]:
        print("✨ Check your browser for the search results!")


if __name__ == "__main__":
    main()
