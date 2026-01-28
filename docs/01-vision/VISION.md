# Health Insurance Provider Search Tool: Vision

**A simple, local tool that eliminates the friction of finding healthcare providers covered by your insurance.**

_(amplifier-health-provider-tool)_

**Owner:** Chris Park  
**Contributors:** Chris Park (with Claude as AI pair programmer)

**Last Updated:** 2026-01-27

---

## Summary

Finding healthcare providers that accept your specific insurance is tedious - you must navigate insurance company websites, enter your location repeatedly, and remember which specialty codes to use. This tool solves that by opening insurance provider directories with search parameters pre-filled based on your stored information. Built for individuals with Premera Blue Cross or Aetna insurance who need quick access to in-network providers for massage therapy, optometry, physical therapy, and other services.

---

## Table of Contents

1. [The Problems We're Solving](#1-the-problems-were-solving)
2. [Strategic Positioning](#2-strategic-positioning)
3. [Who This Is For](#3-who-this-is-for)
4. [The Sequence](#4-the-sequence)
5. [Related Documentation](#5-related-documentation)

---

## 1. The Problems We're Solving

**Solve individual friction points before building complex infrastructure**

### Problem 1: Repetitive Data Entry Wastes Time

#### Every search requires re-entering the same information

**Current Reality:**
- Navigate to insurance website
- Find the provider search page
- Enter zip code every single time
- Select specialty from confusing dropdown menus
- Remember to set search radius
- Repeat for different insurance companies

**The Impact:**
- 5-10 minutes per search wasted on navigation and data entry
- Cognitive overhead remembering specialty codes ("is it Optometry or Vision Care?")
- Frustration leads to delaying necessary healthcare
- Switching between insurance companies requires starting over

**Why This Matters:**
When finding healthcare providers feels like a chore, people delay getting care. The friction isn't just annoying—it's a barrier to healthcare access.

**Who this affects:** Individuals managing their own healthcare appointments

---

### Problem 2: No Programmatic Access to Insurance Directories

#### Insurance companies don't provide APIs for provider searches

**Current Reality:**
- Premera and Aetna have no public APIs
- Web scraping violates Terms of Service
- Bot protection blocks automated access
- Third-party aggregators cost $500-2000/month

**The Impact:**
- Can't build sophisticated provider search tools
- Stuck with manual website navigation
- No way to compare networks programmatically
- Individual developers locked out of the ecosystem

**Why This Matters:**
Insurance companies maintain walled gardens. If you want to build tools to help people find care, you're blocked unless you pay enterprise-level fees or violate ToS.

**Who this affects:** Developers, individual tool builders, people wanting better search experiences

---

### Problem 3: Context Switching Between Providers

#### Comparing provider networks requires multiple manual searches

**Current Reality:**
- Open Premera website, search for massage therapists
- Open Aetna website, search again with same parameters
- Manually compare which network has better options
- No way to see both results side-by-side

**The Impact:**
- Difficult to determine which insurance to use for specific services
- Time-consuming to evaluate network quality
- Miss opportunities to optimize insurance utilization
- Coordination of benefits becomes a manual chore

**Why This Matters:**
People with multiple insurance plans (primary + secondary) need to make informed decisions about which network to use. Manual comparison is tedious and error-prone.

**Who this affects:** People with multiple insurance plans, families managing healthcare across insurances

---

## 2. Strategic Positioning

### The Core Insight

**What is everyone else doing?**

- **Third-party aggregators (Zocdoc, Ribbon Health):** Build web services with API access to multiple insurance networks
- **Insurance companies:** Maintain proprietary directories with no public APIs
- **Browser extensions:** Attempt to scrape insurance websites (fragile, ToS violations)

**Why are they wrong or incomplete?**

They assume the solution must be:
- Cloud-based (requires accounts, subscriptions)
- Complex (full database replication, real-time sync)
- Expensive (API fees, infrastructure costs)

**Your contrarian position**

Most healthcare provider searches don't need real-time data, programmatic access, or sophisticated algorithms. They need **immediate friction reduction** for routine tasks.

**The difference:**
- **Common approach:** Build infrastructure first, solve search later
- **Our approach:** Eliminate friction today with zero infrastructure

Health Insurance Provider Search Tool is built for **immediate utility**, not **comprehensive coverage**.

---

### The 3 Strategic Pillars

#### 1. Local-First

**The old way:** Cloud services with accounts, subscriptions, and data upload  
**The Health Provider Search way:** Everything runs locally, your data stays on your machine

- No accounts, no sign-ups, no cloud dependencies
- Configuration stored in local settings file
- Works offline (opens bookmarked searches)
- Zero privacy concerns (never sends data anywhere)

#### 2. Simplicity Over Sophistication

**The old way:** Build comprehensive databases, scrape provider data, maintain sync  
**The Health Provider Search way:** Open the official insurance website with pre-filled parameters

We don't try to:
- ❌ Maintain our own provider database
- ❌ Scrape insurance websites (ToS violations)
- ❌ Cache or replicate data
- ❌ Provide programmatic search results

We DO:
- ✅ Construct correct URLs with your parameters
- ✅ Open your browser to official sources
- ✅ Let insurance companies maintain the data
- ✅ Stay compliant with Terms of Service

#### 3. Immediate Value

**The old way:** Set up accounts, configure settings, learn complex UIs  
**The Health Provider Search way:** Run one command, browser opens, you're searching

- No installation friction (standalone Python script)
- No learning curve (natural language commands)
- No ongoing maintenance (uses official insurance sites)
- Works in 10 seconds, not 10 minutes

---

### What We're NOT Building

Clear boundaries help AI make correct decisions:

- ❌ Provider aggregation service (we open official sources)
- ❌ API or web service (we're a local tool)
- ❌ Database of providers (insurance companies maintain this)
- ❌ Comparison tool (we open both sites, you compare)
- ❌ Appointment scheduling (we get you to provider info)
- ❌ Multi-insurance support beyond Premera/Aetna (focused scope)

---

## 3. Who This Is For

### Primary: Individuals with Premera or Aetna Insurance

People who regularly need to find healthcare providers and are frustrated by repetitive manual searches.

- People with chronic conditions needing frequent specialist visits
- Parents managing family healthcare appointments
- People exploring alternative medicine (massage, acupuncture, chiropractic)
- Anyone who needs contacts, glasses, or vision care

**Why they're underserved:**
- **Third-party services**: Require accounts, have gaps in coverage, cost money
- **Insurance websites**: Require manual navigation every single time
- **Browser bookmarks**: Don't pre-fill your specific search parameters

### Secondary: Developers Building Healthcare Tools

Developers who want to build personal tools but are blocked by lack of APIs.

- Hackers/makers who solve their own problems
- People learning to build tools with AI assistants
- Folks interested in "local-first" software philosophy

**What they need:**
- Working example of compliant healthcare tool building
- Pattern for URL construction and parameter mapping
- Demonstration that simple solutions can work

---

## 4. The Sequence

**Individual utility → Multiple providers → Extensibility**

**We solve one person's friction first, then expand capabilities.**

### V1: Single-User Standalone Tool (CURRENT)

**Focus:** Eliminate search friction for one person with Premera/Aetna insurance

**Core capabilities:**
- Store insurance info and location locally
- Map natural language service types to specialty codes
- Construct correct URLs for Premera and Aetna
- Open browser with pre-filled search parameters
- Support primary and secondary insurance selection

**V1 validates:** Do people actually use a simple command-line tool for this? Does eliminating data re-entry save meaningful time?

**V1 reality:** Fully implemented as standalone Python script. Works perfectly for the target use case. Not yet integrated as Amplifier bundle (Tool protocol integration attempted but deferred due to complexity vs. value).

---

### V2: Enhanced UX & More Providers (FUTURE)

**Focus:** Make the tool even easier to use and support more insurance companies

**Core capabilities:**
- GUI or menu-driven interface (less typing)
- Support for additional insurers (Blue Cross, UnitedHealthcare, Kaiser)
- Provider result caching (remember recent searches)
- Smart search history (suggest recently used services)
- Shell aliases generation (automated setup)

**V2 goal:** Expand beyond power users to anyone comfortable running local tools

---

### V3: Optional Programmatic Access (MAYBE)

**Focus:** Enable optional integration with third-party APIs for users who want it

**Core capabilities:**
- Optional Ribbon Health API integration (for programmatic results)
- In-conversation result display (via Amplifier integration)
- Provider comparison across insurances (side-by-side)
- Appointment scheduling links (if APIs become available)

**V3 goal:** Provide sophistication as an opt-in for users who want it, keeping simplicity as default

---

## 5. Related Documentation

**Vision folder (strategic context):**
- This document provides the complete strategic context

**Current features and roadmap:**
- [docs/README.md](../README.md) - Epic table showing implementation status
- [docs/02-requirements/epics/](../02-requirements/epics/) - Detailed feature requirements

**Implementation guidance:**
- [README.md](../../README.md) - Project README with usage instructions
- [search_providers.py](../../search_providers.py) - Standalone script implementation

---

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-01-27 | Chris Park | Initial vision document |

---

## Writing Guidelines

**Purpose of Vision Document:**
- Define the problems in the world that need solving
- Articulate strategic positioning (how you're different)
- Identify target audience and why they're underserved
- Explain sequencing and phase strategy
- Provide decision-making context for AI (80% of purpose)

**WHAT to include:**
- User problems (real pain points)
- Strategic differentiation (your unique positioning)
- Target audience (who you're building for)
- Sequencing rationale (why this order)
- Clear boundaries (what you're NOT building)

**WHAT to exclude:**
- Implementation details (those go in principles)
- Feature specifications (those go in epics)
- Success metrics (separate doc: 04-SUCCESS-METRICS.md)
- Competitive details (separate doc: 03-COMPETITIVE-ANALYSIS.md)
- Technical architecture (goes in dev-design/)

**For AI context (80%):**
- Make it decision-enabling (helps AI choose correctly)
- Provide clear boundaries (prevents building wrong things)
- Explain WHY, not just WHAT
- Keep scannable with clear section headers

**For human readers (20%):**
- Executive summary at top
- Logical flow (problems → positioning → audience → sequence)
- Readable without technical background

**Test:** Can AI use this to make correct product decisions? Can a non-technical person understand the strategic direction?

---

**Questions?** See existing vision docs in docs/01-vision/ for examples.


