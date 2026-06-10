# Patent Analyzer — Quick Reference


## Input

| Parameter | Source | Required? |
|---|---|---|
| Asset name / active ingredient | User | Yes |
| Modality (small molecule, biologic, etc.) | User | Yes |
| Patent numbers (if known) | User / Orange Book / SEC filings | Recommended |
| Company name (for patent assignment search) | User | Yes |
| Therapeutic indication | User | Recommended |

## Quick Reference

| Patent Type | Protection Strength | Vulnerability | Duration |
|---|---|---|---|
| Composition of Matter (CoM) | Strongest — covers the molecule itself | Hardest to design around | Filing date + 20 years + PTE |
| Salt / Polymorph | Strong — covers specific forms | Designable if alternative forms exist | Filing + 20 + PTE |
| Formulation | Moderate — covers delivery method | Generics can reformulate | Filing + 20 + PTE |
| Method of Use | Moderate — covers specific indication | Does not prevent off-label use of generic; skinny label strategies | Filing + 20 + PTE |
| Dosing Regimen | Weak-Moderate — covers specific dose/schedule | Difficult to enforce; physicians may prescribe off-label | Filing + 20 |
| Process / Manufacturing | Weakest for exclusivity — covers how to make it | Alternative processes usually possible | Filing + 20 |
| Combination | Variable — covers specific drug combinations | Only protects the combination, not individual components | Filing + 20 + PTE |

## Quick Reference

| Factor | Low Risk | High Risk |
|---|---|---|
| CoM patent strength | Strong, validated CoM | No CoM; only method-of-use/formulation |
| Prior art | Clean prosecution history | Multiple rejections, narrow claims |
| Peak sales | <$500M (limited generic incentive) | >$1B (strong generic incentive) |
| Patent scope | Broad genus claims covering analogs | Narrow species claims |
| Litigation history | No IPR challenges; clean IPR record | IPR losses; claim narrowing |
| Number of generic filers | 0-1 ANDA filers | Multiple ANDA filers |

## Quick Reference

| FTO Dimension | Assessment | Risk |
|---|---|---|
| Compound/composition | Does any third party hold CoM claims covering the molecule or genus? | [High/Med/Low] |
| Target biology | Are there patents on the biological target that could create royalty obligations? | [High/Med/Low] |
| Technology platform | Does the platform (mAb engineering, AAV capsid, LNP formulation) have IP encumbrances? | [High/Med/Low] |
| Manufacturing process | Do process patents create manufacturing method restrictions? | [High/Med/Low] |
| Formulation/delivery | Are there delivery technology patents that apply? | [High/Med/Low] |

## Quick Reference

| Patent # | Type | Filing Date | Expiry | PTE/PTA | Effective Expiry | Strength |
|----------|------|-------------|--------|---------|------------------|----------|
| US X,XXX | CoM  | [date]      | [date] | +[X]mo  | [date]           | Strong   |
| US X,XXX | MoU  | [date]      | [date] | N/A     | [date]           | Moderate |
| ...      |      |             |        |         |                  |          |

## Error Handling

| Scenario | Response |
|---|---|
| Patent numbers not available | Search USPTO, Espacenet, Google Patents by assignee + compound name |
| No Orange/Purple Book listing | Asset may be pre-approval; analyze patent applications and granted patents directly |
| International patent variations | Note US vs EU vs ROW expiry differences; model revenue by geography |
| Patent challenge pending (IPR/PGR) | Flag as active risk; model scenarios with and without challenged claims |
