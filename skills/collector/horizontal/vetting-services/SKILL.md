---
name: vetting-services
description: >
  Vet the appraisers, graders, dealers, and auction houses themselves. Use when selecting an
  appraiser for tax / insurance / estate purposes, deciding which grading service to send a
  raw item to, evaluating a dealer's credentials, reading auction-house lot descriptions for
  what is *not* said, or interpreting attribution language. Covers USPAP compliance, the
  AAA/ASA/ISA appraiser credentials, CINOA/ADAA dealer associations, and the attribution
  hierarchy that catalog language uses to encode warranty exposure.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Vetting Services — Authentication of the Authenticators

> **Type:** Knowledge
> **Suite:** The Collector
> **Axis:** Horizontal
> **Parent:** collector

## The Meta-Discipline

Authenticity, condition, and pricing all depend on third parties — appraisers, graders, dealers, auction houses, scholars. The collector's most leveraged skill is not knowing the assets — it is knowing the people and institutions who certify them.

The market for trust is itself a market. It has standards, certifications, professional associations, ethics codes, and reputational sanctions. A collector who can read this meta-market avoids 80% of the costliest mistakes.

## Qualified Appraisers — The Legal Bar

For US tax purposes (Form 8283 charitable contributions over $5,000, estate tax filings, insurance scheduling), an appraisal must be done by a **qualified appraiser** as defined in IRS regulations and Treasury Circular 230.

### The Three Major Credentialing Bodies

| Body | Acronym | Notes |
|---|---|---|
| **Appraisers Association of America** | AAA | Founded 1949; strong on fine art, decorative arts, jewelry; rigorous Accredited Member (AAA) and Certified Member (CAAA) designations |
| **American Society of Appraisers** | ASA | Founded 1936; broader (machinery, real estate, business valuation, personal property); Accredited Senior Appraiser (ASA) is the senior designation |
| **International Society of Appraisers** | ISA | Founded 1979; strong on personal property; ISA Accredited Member (AM) and Certified Appraiser of Personal Property (CAPP) designations |

All three bodies require:

- Initial coursework and examination
- USPAP compliance (15-hour course plus 7-hour update every 2 years)
- Specialty-specific competency demonstration
- Ongoing CE and ethics adherence

### USPAP Compliance

**Uniform Standards of Professional Appraisal Practice**, maintained by the Appraisal Foundation. Every legitimate US appraisal should declare USPAP compliance on its face. The IRS will reject an appraisal without USPAP compliance for tax purposes.

USPAP-compliant reports include:

- Identification of the property and the appraiser
- Statement of the appraisal's intended use and intended users
- Type and definition of value (FMV, replacement value, marketable cash value)
- Effective date of value
- Scope of work performed
- Description of the property and its condition
- Analysis of comparable sales / valuation methodology
- Reconciliation and final value conclusion
- Signed certification

### Conflict-of-Interest Rules

A qualified appraiser cannot:

- Be the donor, donee, or party to the transaction being appraised
- Charge a contingent fee tied to the appraised value
- Have an undisclosed relationship with the dealer or auction house that sold the item
- Have been disqualified by the IRS in the past three years

## Dealer Vetting

The dealer is the curriculum. A trusted dealer is the single highest-yield asset a beginning collector can acquire. Vetting a dealer means checking:

### Professional Associations

| Association | Acronym | Coverage |
|---|---|---|
| **Confédération Internationale des Négociants en Œuvres d'Art** | CINOA | International (~5,000 dealers across 40 associations); the umbrella body |
| **Art Dealers Association of America** | ADAA | US; ~180 vetted member galleries; founded 1962 |
| **Private Art Dealers Association** | PADA | US-based private dealers |
| **British Antique Dealers' Association** | BADA | UK; rigorous vetting; founded 1918 |
| **Society of London Art Dealers** | SLAD | UK; established 1932 |
| **American Booksellers' Association** | ABAA | US rare books; founded 1949 |
| **International League of Antiquarian Booksellers** | ILAB | International rare books |
| **American Numismatic Association** | ANA | US coins; member dealer directory |
| **Professional Numismatists Guild** | PNG | US coins; stricter vetting; ~300 dealer-members |
| **Watch & Clock Dealers** | Various national bodies | Less centralized internationally |

A member dealer in a vetted association signals reputational accountability — bad behavior can result in expulsion, which is a meaningful sanction in trade circles where reputation is the asset.

### Red Flags in a Dealer Relationship

- **No physical premises** — Internet-only dealers can be legitimate but warrant additional vetting
- **No willingness to provide provenance documentation** — a dealer who can't or won't show chain of custody is signaling
- **Pressure to close fast** — "this won't last; another buyer is on the way; need to know by tomorrow"
- **Reluctance to allow independent expertise / second opinions** — a confident dealer welcomes second opinions; an evasive one resists
- **Inability to provide bank-traceable payment terms** — cash-only or unusual payment routing
- **Vague or evolving provenance stories** — the story should be the same in every retelling

## Grading Services — Service-Specific Vetting

Each major grading service has a different track record. The vetting questions:

- **Population report depth** — how many cards / coins / comics has the service graded in your category?
- **Market acceptance** — do dealers pay equivalent prices for items in this service's slabs vs. the dominant alternative?
- **Track record on disputes** — has the service been involved in major scandals (PSA reholder/trimming 2019, CGC defamation 2024)?
- **Customer service** — turnaround times, communication, post-sale support
- **Pop / value transparency** — do they publish accessible data, or is the data behind paywalls?

PSA, CGC, BGS, SGC, PCGS, NGC are the major names; each has strengths and historical incidents the collector should know.

## Reading Auction-House Lot Descriptions

The catalog hedge — auction houses use cautious language exactly when they cannot warrant something. The transferable skill is reading what is *not* said.

Refer to `references/attribution-hierarchy.md` in the orchestrator for the full taxonomy. Critical phrases:

- **Full attribution name with no qualifier** → 5-year limited authenticity warranty
- **"Attributed to"** → warranty withdrawn; major value discount
- **"Studio of" / "Circle of" / "Follower of" / "Manner of" / "After"** → descending tiers of warranty and value
- **"Bears signature"** → the signature is explicitly disclaimed
- **"Provenance: Private collection, Europe"** → provenance being deliberately obscured

The auction house's Conditions of Sale (back of the catalog or online) define exactly what they warranty and what they disclaim. Read these before bidding.

## The Catalog Hedge in Other Domains

| Domain | Hedging Phrase | What It Means |
|---|---|---|
| Watches | "We believe the dial is original" (vs "The dial is original") | The house is signaling uncertainty |
| Wine | "European collection" (vs "ex-château" or "ex-cellar of [named collector]") | Provenance is being obscured |
| Cards | "Card has been pressed" or silence on pressing | Disclosure status matters for resale ethics |
| Comics | "Restoration: undetectable" (vs "Universal grade" blue label) | Has been graded but the restoration assessment is the critical detail |
| Books | "Condition: very good plus, with usual restorations" | "Usual restorations" can hide significant work |

## Workflow — Vetting a Service or Dealer Before Engagement

1. **Identify the relevant associations** for the asset class and check membership
2. **Search for disciplinary actions** — most associations publish disputes, expulsions, censures
3. **Look for the LinkedIn / professional bio** of the principal — credentialed appraiser? Years in trade? Specific expertise?
4. **Read the firm's published work** — articles, lot essays, catalogs, lectures
5. **Ask for three client references** — and actually call them
6. **Run a Google search with "[dealer name] dispute" / "lawsuit" / "complaint"**
7. **Use a small first transaction to test** — a $1K acquisition before a $50K one; observe the entire process
8. **Verify USPAP compliance on any appraisal** — refuse to use an appraisal that doesn't claim USPAP

---

Connoisseur ─── The Dealer Is the Curriculum

Goldberger's "buy the seller, not the watch" is the most transferable wisdom in collecting. A trusted dealer over fifteen years will teach the user more, save the user more money, and bring the user more important pieces than any twenty courses or fifty books. The dealer's reputation is on the line in every transaction; the user's relationship compounds across decades. Cultivate three dealers in any asset class you care about; meet them in person; spend time at their shop or booth; ask questions and listen more than you talk. This is the most reliable curriculum in collecting.

Allocator ─── Vetting Cost Is Cheaper Than Mistake Cost

A formal appraisal from a USPAP-compliant AAA/ASA/ISA appraiser costs $500–3,000 for most items. A failed authentication, a denied charitable deduction, an underinsured loss, or a fraudulent acquisition costs orders of magnitude more. The IRS Art Advisory Panel reviews appraisals above $50K per item; the panel's denial rate on aggressive appraisals exceeds 60% in some categories. The cost of upfront vetting — qualified appraiser, vetted dealer, verified COA chain — is the cheapest insurance on the largest mistakes. Pay it.
