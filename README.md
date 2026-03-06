# amplifier-health-provider-tool

**This project failed. That's the point.**

I tried to build an AI tool that finds healthcare providers accepting specific insurance (Premera Blue Cross + Aetna) near Issaquah, WA. It doesn't do that. This repo is published anyway — because documenting a failure clearly is more useful than pretending it didn't happen.

---

## What I Actually Learned (The Centerpiece)

**1. AI can't fix a data availability problem.**
I kept trying to find a clever technical workaround. There wasn't one. The data simply isn't free. That's a business constraint, not an engineering challenge — and no amount of prompting or API-chaining changes it.

**2. Find the blocker before you build the interface.**
I built a CLI, wrote documentation, and wired up NPI lookups before confirming the core data existed. Classic mistake. The right order: validate the critical dependency first, build everything else second.

**3. Knowing when to stop is a product skill.**
Iterating on a solvable problem is persistence. Iterating on an unsolvable one is just sunk cost. The call to archive this was the right product decision.

**4. The documentation outlived the tool.**
Used a doc-driven-dev workflow throughout. The vision doc, the epic, the honest failure analysis — all of it holds up. Good process produces good artifacts even when the product doesn't ship.

---

## Why It Failed

**The fundamental blocker:** No free API exists for insurance network verification.

| Approach | What I Tried | Why It Failed |
|---|---|---|
| URL construction | Deep-link into insurance sites with pre-filled filters | JavaScript SPAs ignore URL parameters entirely |
| CMS NPI Registry | Free government API for provider lookup | Returns name/address/phone — zero insurance data |
| Web scraping | Parse insurance provider directories | Protected against scraping |

**The only solution that actually works:** [Ribbon Health API](https://h1.co/request-demo/) — $500–2,000/month, enterprise only.

---

## What Got Built (Despite Everything)

A Python CLI that searches the CMS NPI Registry by specialty near a zip code. Supports fuzzy specialty lookup ("contacts" → optometrist, "chiro" → chiropractor). Opens insurance websites in browser tabs for manual search.

Honest assessment: *slightly faster than Google, basically just Yelp but worse.*

```bash
python3 search_providers.py "massage therapy" --limit 10
```

It works. It just doesn't solve the problem I wanted to solve.

---

## Why This Is Public

Most builders quietly delete the repos that didn't work out. I think that's wrong.

This repo demonstrates something that matters more than the tool itself: the ability to find a real blocker, name it clearly, document what was tried, and make the call to stop. That's product discovery. It's harder than it sounds, and it doesn't always produce something shippable.

Publishing it is intentional. The learning value is higher than zero. The product value is not.

---

## Built By

**Chris Park** — Senior PM, Microsoft Office of the CTO, AI Incubation.

17 years in product. Brand: *"PM who actually builds — including the things that don't work."*

---

## License

MIT
