# Health Insurance Provider Search Tool

**Status: ⚠️ FAILED EXPERIMENT - Does Not Solve The Problem**

This project was an attempt to build an AI-driven tool for finding healthcare providers that accept specific insurance (Premera Blue Cross and Aetna). **It does not work** for the intended use case.

## What Was Attempted

Build a tool that lets you say "find massage therapists that accept my Premera insurance" and get a useful answer.

## Why It Failed

**The fundamental problem:** No free API exists for insurance network verification.

### What We Tried:

1. **URL Construction** ❌
   - Attempted to open insurance websites with pre-filled search parameters
   - Reality: Insurance sites use JavaScript SPAs that ignore URL parameters
   - Result: Opens to search page, but user must manually enter everything

2. **CMS NPI Registry** ❌
   - Free government API that returns provider lists
   - Reality: Only provides basic directory info (name, address, phone)
   - **Critical limitation:** NO insurance network data
   - Result: Just a phone book - user must call each provider to verify insurance

### The Only Solution That Works:

**Ribbon Health API** (enterprise pricing, contact sales)
- https://h1.co/request-demo/
- Estimated cost: $500-2000/month
- This is the ONLY service with programmatic insurance network verification

## What Actually Got Built

### Working Components:

**1. NPI Provider Search** (`search_providers.py`)
```bash
python3 search_providers.py "massage therapy" --limit 10
```
Returns list of providers with:
- Name, specialty, address, phone, license
- **Does NOT verify insurance acceptance**
- User must call each provider manually

**2. Insurance Website Launcher** (`--mode insurance`)
```bash
python3 search_providers.py "massage therapy" --mode insurance
```
Opens Premera/Aetna search pages (no pre-filled parameters)

### What This Actually Provides:

- Slightly faster than Google search
- Organized provider list with phone numbers
- **Still requires manual insurance verification for every provider**
- Basically just Yelp but worse

## Documentation (The Only Success)

Used the doc-driven-dev workflow to create:
- `docs/01-vision/VISION.md` - Strategic vision (problems, positioning, roadmap)
- `docs/02-requirements/epics/01-provider-search.md` - Epic documentation
- Complete documentation structure following templates

**This documentation process worked great.** The tool itself did not.

## Installation (If You Want to Try It Anyway)

```bash
cd ~/amplifier-health-provider-tool
python3 search_providers.py "massage therapy" --limit 10
```

Configuration in the script at line 15 (CONFIG dictionary).

## Lessons Learned

1. **Validate APIs exist before building** - Should have confirmed NPI Registry includes insurance data
2. **Don't build around assumptions** - Assumed insurance sites support URL parameters (they don't)
3. **Be honest about limitations early** - Should have said "this needs a paid API" from the start
4. **Testing matters** - Should have tested with real API calls before building the interface

## If You Actually Want This Feature

**Pay for Ribbon Health API:**
- Request demo: https://h1.co/request-demo/
- Ask about Premera and Aetna support
- Get pricing quote
- Integrate their API (replace NPI client with Ribbon client)

## License

MIT License

## Status

**Archived** - Does not solve the intended problem without paid API access.
