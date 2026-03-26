# Market Design Case Studies

## Case 1: National Resident Matching Program (NRMP)

### History

The medical residency market is the longest-running example of successful market design.

**Pre-1945**: No organized matching. Hospitals competed by making earlier and earlier offers — eventually offering positions to students in their second year of medical school, before clinical rotations. Students had to accept or reject before knowing their options.

**1945-1951**: Centralized matching attempted through various systems. Early algorithms favored hospitals.

**1952**: NRMP established using an algorithm designed by John Stalmaker and colleagues. Roth (1984) later showed this algorithm was equivalent to hospital-proposing Gale-Shapley DA.

**1995-1998**: Redesign. The original algorithm was hospital-proposing (hospital-optimal). Roth and Peranson (1999) redesigned to applicant-proposing (applicant-optimal). Also added:
- **Couples matching**: Medical student couples submit paired rank order lists. The algorithm accommodates couples by using a modification of DA with iterative adjustment for complementarities. This problem is NP-hard in general, but the Roth-Peranson algorithm works well in practice.
- **Supplementary offer programs**: Additional matching rounds for unfilled positions.

### Current Scale

~35,000 applicants matched annually through the Main Residency Match, plus specialty matches. Over 47,000 applicants submitted rank order lists in 2024.

### Key Lesson

Centralized clearinghouses succeed when they're thicker, safer, and less congested than the decentralized alternative. The NRMP persists because it benefits both sides — hospitals get committed residents, applicants get fair access to positions.

## Case 2: NYC School Choice

### The Problem (Pre-2003)

New York City assigned ~80,000 students to 500+ high school programs annually. The old system:
- Students submitted a preference list of up to 5 schools
- Schools processed lists sequentially using proprietary criteria
- No coordination between schools
- Result: ~30,000 students unmatched in the main round, assigned administratively
- Wealthy/connected families could game the system; unsophisticated families were disadvantaged

### The Redesign (2003)

Atila Abdulkadiroglu, Parag Pathak, and Alvin Roth designed a student-proposing DA mechanism:
- Students submit a rank-ordered list of up to 12 programs
- Programs rank students using disclosed priority criteria (grades, test scores, geographic zones, etc.)
- DA runs centrally
- Students can rank truthfully without strategic risk (strategy-proof for students)

### Results

- Unmatched students dropped from ~30,000 to ~3,000
- Students received higher-ranked choices on average
- Eliminated the advantage of sophisticated families who could game the old system
- More students assigned to first- or second-choice schools

### Key Lesson

Strategy-proofness is a fairness property. When the mechanism is manipulable, sophisticated players exploit it. DA levels the playing field by making honest preference reporting optimal.

## Case 3: Kidney Exchange

### The Problem

~100,000 patients wait for kidney transplants in the US. ~5,000 die annually waiting. Many have willing living donors who are biologically incompatible.

### The Innovation (2004+)

Roth, Sonmez, and Unver (2004) proposed kidney exchange: incompatible patient-donor pairs can swap donors.

**Pairwise exchange**: Patient A's donor gives to Patient B; Patient B's donor gives to Patient A. Requires simultaneous surgeries (if one side reneges, the other loses their donor).

**Chains from non-directed donors (2006+)**: An altruistic donor (no paired patient) starts a chain. Their donation triggers a cascade — each recipient's paired donor donates to the next patient.

**Non-Simultaneous Extended Altruistic Donor (NEAD) chains**: The breakthrough. Because chains don't need simultaneous surgery (each donor gives before their paired patient receives), chains can extend much longer than cycles. A single altruistic donor can trigger 10+ transplants.

### Current Scale

- ~550 kidney exchange transplants/year in the US (2020s)
- Multiple exchanges operate: National Kidney Registry (NKR), Alliance for Paired Kidney Donation (APKD), UNOS KPD
- Some chains have exceeded 30 transplants from a single altruistic donor

### Key Lesson

Market design can create value from nothing — patients and donors who couldn't help each other can help each other through cycles and chains. The key insight was that "repugnant transactions" (selling kidneys) can be replaced by "acceptable transactions" (exchanging donations).

## Case 4: Spectrum Auctions (FCC)

### Early History

Pre-1993: FCC allocated spectrum through "beauty contests" (subjective evaluation of applications) and lotteries. Both methods were inefficient — licenses went to applicants who were poor at extracting value, and secondary markets were thin.

### The Auction Solution (1994+)

Congress authorized spectrum auctions in 1993. Milgrom and Wilson designed the Simultaneous Multiple Round (SMR) format:
- All licenses auctioned simultaneously
- Bidders can shift demand across licenses as prices evolve
- Activity rules ensure genuine participation
- Price discovery through ascending rounds

### The Incentive Auction (2016-2017)

The most complex auction ever designed. Two-sided: a **reverse auction** repurchased TV spectrum from broadcasters, and a **forward auction** sold that spectrum to wireless carriers.

Challenges solved:
- **Repacking**: After buying some broadcasters' spectrum, remaining broadcasters must be reassigned channels to clear contiguous blocks for wireless use. An NP-hard feasibility problem.
- **Revenue target**: Forward auction revenue must exceed reverse auction costs plus relocation expenses.
- **Incentive compatibility**: Both sides must have incentives to participate honestly.

Result: Cleared 84 MHz of spectrum, generated $19.8B in gross revenue, with $10.05B going to broadcasters and $7.3B in net proceeds.

## Case 5: Online Platforms and Two-Sided Matching

### Ride-Sharing (Uber/Lyft)

Not a traditional matching market, but a real-time matching problem with transfers. The platform matches riders to drivers, sets prices (surge pricing), and manages participation incentives.

Game-theoretic issues:
- **Surge pricing as mechanism design**: Dynamic pricing balances supply and demand in real time
- **Driver strategy**: When to drive, where to position, whether to accept rides
- **Platform competition**: Uber vs. Lyft competition for drivers and riders resembles a two-sided market platform game

### Online Dating

Two-sided matching with partial information. Platforms design recommendation algorithms, messaging limits, and matching rules.

Key design issues:
- **Congestion**: Without constraints, everyone messages the most popular users, who become overwhelmed
- **Information design**: How much profile information to reveal affects matching quality
- **Thick vs. safe tradeoff**: Larger platforms are thicker but may be less safe (spam, misrepresentation)
