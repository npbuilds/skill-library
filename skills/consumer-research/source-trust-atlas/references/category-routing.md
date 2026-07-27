# Category Routing & Query Templates

Per-category source chains and site-scoped query templates for the emptor scan phase. Rule zero: **no generic "best X" queries** — always site-scope.

## Electronics — TV / audio / monitors / peripherals

- Chain: Rtings → Consumer Reports → Wirecutter; Reddit (r/hometheater, r/headphones…) second-pass only.
- Templates:
  - `site:rtings.com <product type> <key constraint>`
  - `site:consumerreports.org <product type> ratings`
  - `site:wirecutter.com best <product type>` (Tier 2 — corroboration)
- Decay: 12mo (T1) / 6mo (T2). Check whether the tested model year matches the current SKU.

## Major appliances — laundry, refrigeration, HVAC

- Chain: Consumer Reports → Which? → Wirecutter; owner forums for long-term reliability anecdotes (hypothesis only).
- Templates: `site:consumerreports.org <appliance> reliability`, `site:which.co.uk <appliance> review`
- Prioritize predicted-reliability and repair-frequency data over feature scores.

## Kitchen gear

- Chain: America's Test Kitchen → Wirecutter → GH Institute.
- Templates: `site:americastestkitchen.com <item> review`, `site:wirecutter.com <item>`

## Tools / outdoor / hardware / automotive consumables

- Chain: Project Farm → Consumer Reports → Wirecutter.
- Templates: `site:youtube.com project farm <item>`, `site:consumerreports.org <item>`

## Software / SaaS

- Chain: Capterra/G2 (verified + recent only) → TechRadar/CNET hands-on reviews → official changelogs.
- Templates: `site:capterra.com <category> reviews`, `site:techradar.com <product> review <current year>`
- Decay: 3 months. Any review without a visible test/update date is unusable. Pricing pages are the only spec source — re-fetch, never recall.

## Services — trades, repair, local

- No institutional source exists (lowest-confidence category; say so in the brief).
- Chain: local subreddit/Nextdoor threads with astroturf protocol → Google/Yelp reviews filtered for detail + verified visits → licensing-board lookups → word-of-mouth.
- Astroturf protocol per thread: account age > 6mo, posting history beyond the one business, specifics that could be falsified, presence of mixed sentiment.

## Cross-category rules

1. Candidate pool target: 15-50 from Tier 1-2 before elimination; if Tier 1 coverage is thin, widen to Tier 2 and lower the brief's overall confidence ceiling one notch.
2. Paywalled Tier 1 reviews (CR, Which?) on critical claims → route to `paywall-strategist` before declaring unverifiable.
3. Every fetched price/availability fact carries its fetch date.
4. When two Tier 1 sources disagree, report the disagreement (Contested) — do not average it away.
