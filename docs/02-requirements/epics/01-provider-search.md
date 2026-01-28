# Epic 01: Insurance Provider Search

**Owner:** Chris Park  
**Contributors:** Chris Park (with Claude as AI pair programmer)

<!--
Derive ownership and history from git - don't guess or assume:

Contributors by commit count:
git log --format="%an" -- <relevant-files> | sort | uniq -c | sort -rn

Full history with dates:
git log --format="%ad %an - %s" --date=short -- <relevant-files>

Example: git log --format="%an" -- "backend/src/agent/*.ts" | sort | uniq -c | sort -rn
-->

---

## 1. Summary

A standalone command-line tool that opens insurance company provider directories with search parameters pre-filled based on stored user configuration. Users can search for healthcare providers (massage therapists, optometrists, physical therapists, etc.) without repeatedly entering location and insurance information.

---

## 2. Problem

Finding healthcare providers that accept specific insurance requires:
- Navigating to insurance company website
- Entering zip code and location every time
- Selecting specialty from confusing dropdown menus
- Remembering which insurance to use (primary vs secondary)
- Repeating the entire process for different services

This creates 5-10 minutes of friction per search and causes people to delay finding healthcare providers.

---

## 3. Proposed Solution

A local Python script that:
- Stores user's insurance info and location in configuration
- Accepts natural language service descriptions ("massage therapy", "contact lenses")
- Maps service types to insurance specialty codes
- Constructs correct URLs for insurance provider directories
- Opens browser with search pre-filled
- Supports searching primary insurance, secondary insurance, or both

Users run a simple command like `python3 search_providers.py "massage therapy"` and their browser opens to the insurance provider directory with everything pre-filled.

---

## 4. User Stories

**IMPORTANT:** Only include user stories for IMPLEMENTED features. Do NOT create user story files for future work. Epic describes future capabilities, but detailed user story files are created when ready to build.

### Implemented

| # | Story | Owner | Created | Contributors | Last Updated |
|---|-------|-------|---------|--------------|--------------|
| - | All V1 functionality | Chris Park | 2026-01-27 | - | - |

**Note:** This epic was documented retroactively after implementation. User stories were not written in advance per the doc-driven philosophy (only create user stories for implemented features).

### Future

- ⏭️ **GUI interface** - Visual menu for selecting services instead of command line
- ⏭️ **Additional insurers** - Support Blue Cross, UnitedHealthcare, Kaiser
- ⏭️ **Search history** - Remember and suggest recently searched services
- ⏭️ **Provider caching** - Cache recent search results locally
- ⏭️ **Amplifier bundle integration** - Use as conversational tool in Amplifier sessions

---

## 5. Outcomes

**Success Looks Like:**
- User can search for providers in under 10 seconds (vs 5-10 minutes manually)
- Zero data re-entry (location and insurance stored once)
- 100% compliant with insurance ToS (no scraping, uses official sites)
- Works reliably across macOS environments

**We'll Measure:**
- Time saved per search (target: 90% reduction)
- Frequency of use (indicates actual value)
- Number of different service types searched (validates natural language mapping)

---

## 6. Dependencies

**Requires:** 
- Python 3.11+ installed
- User has Premera and/or Aetna insurance
- macOS environment (or Python environment with webbrowser support)

**Enables:** 
- Reduced friction for routine healthcare provider searches
- Pattern for building compliant healthcare tools
- Foundation for optional Amplifier integration

**Blocks:** 
- None (this is foundational functionality)

---

## 7. Risks & Mitigations

| Risk | Impact | Probability | Strategic Response |
|------|--------|-------------|-------------------|
| Insurance websites change URL structure | H | M | Monitor for breakage, update URL builders. Official sites change infrequently. |
| Users don't adopt command-line tool | M | M | Create GUI wrapper or shell aliases for easier access. V1 validates core value. |
| Natural language mapping misses specialty types | L | L | Expand mapping dictionary based on user feedback. Easy to add new mappings. |
| Limited to two insurance companies | M | H | Acceptable for V1. Most users have 1-2 insurers. Expand in V2. |

---

## 8. Open Questions

- [x] Should this be integrated into Amplifier as a bundle? **Decision: Standalone first, bundle optional. Integration attempted but complexity didn't justify value for single-user tool.**
- [ ] What other insurance companies should be prioritized for V2?
- [ ] Would users prefer GUI over command-line?
- [ ] Should configuration live in settings.yaml or in the script itself?

---

## 9. Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-01-27 | Chris Park | Initial epic (retroactive documentation) |

---

## Writing Guidelines

**WHAT to include:**
- User problems and needs
- Capabilities and experiences
- Outcomes and success metrics
- Strategic decisions

**WHAT to exclude:**
- Technical details (code, APIs, schemas)
- UI specifics (buttons, toolbars, components)
- Implementation mechanisms (metadata, endpoints)
- Timelines or estimates

**Test:** Can a non-technical person (CEO, investor) understand this without technical knowledge?


