---
name: manufacturing-ip
description: >
  Direct CMC risk assessment, modality-specific manufacturing analysis, patent landscape mapping,
  and IP valuation questions to the appropriate specialist skill. Activate when evaluating
  manufacturing feasibility, COGS trajectory, freedom-to-operate, patent life, or IP-driven
  asset value. Manufacturing and IP are the most commonly underweighted pillars in biotech
  diligence — this director ensures they receive rigorous, modality-aware analysis.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Manufacturing & IP Director

Manufacturing and intellectual property are the pillars that venture investors most frequently underweight — and the ones that most frequently destroy value in late-stage programs. A gene therapy with a manufacturing yield problem can become commercially unviable regardless of clinical efficacy. A small molecule with a weak patent estate can face generic erosion within years of launch. This director routes manufacturing and IP questions to specialist skills that analyze these risks with the rigor they deserve.

## Child Skills

| Skill | Type | When to Use |
|-------|------|-------------|
| cmc-risk-assessor | action | Assessing chemistry, manufacturing, and controls risk — process scalability, analytical comparability, formulation stability, supply chain vulnerability, facility readiness, and CMC-related regulatory risk |
| modality-manufacturing | knowledge | Understanding modality-specific manufacturing considerations — small molecule synthesis, biologics cell line development, ADC conjugation, gene therapy vector production, cell therapy autologous vs allogeneic, mRNA-LNP manufacturing, oligonucleotide synthesis |
| patent-analyzer | action | Mapping the patent landscape — composition of matter, method of use, formulation patents, patent term adjustments, patent term extensions, paragraph IV exposure, IPR/PGR vulnerability, and freedom-to-operate analysis |
| ip-valuation | knowledge | Understanding IP-driven asset value — patent life impact on rNPV, biosimilar/generic erosion curves, trade secret vs patent strategies, licensing implications of IP strength, and regulatory exclusivity periods (NCE, orphan, pediatric, biologics) |

## Routing Logic

| Question Signal | Route To | Examples |
|-----------------|----------|----------|
| CMC, manufacturing risk, process scalability, analytical methods, comparability, formulation, supply chain | cmc-risk-assessor | "What are the CMC risks for this gene therapy program?" / "Can they scale manufacturing?" |
| Modality, manufacturing process, cell line, vector production, conjugation, synthesis, COGS | modality-manufacturing | "What are the manufacturing challenges for AAV gene therapies?" / "How does ADC manufacturing differ from standard biologics?" |
| Patent, IP landscape, freedom-to-operate, patent life, patent cliff, paragraph IV, IPR | patent-analyzer | "What does the patent estate look like?" / "When does patent protection expire?" |
| IP value, patent impact on valuation, biosimilar erosion, exclusivity, generic entry | ip-valuation | "How does the patent cliff affect valuation?" / "What exclusivity protections does this asset have?" |
| Manufacturing + IP together | cmc-risk-assessor then patent-analyzer | "Full manufacturing and IP diligence" |
| COGS + IP value | modality-manufacturing then ip-valuation | "What are COGS implications and how long is the IP runway?" |

## Multi-Skill Questions

1. **CMC + Modality**: "Can this gene therapy program scale to commercial manufacturing?"
   - Load modality-manufacturing for AAV-specific manufacturing considerations (vector yield per batch, full/empty capsid ratio, scalability of suspension vs adherent processes)
   - Load cmc-risk-assessor to evaluate the specific program's manufacturing readiness, process development stage, and CMC regulatory risk
   - Synthesize: Modality knowledge provides the framework; CMC risk assessment applies it to the specific program. Gene therapy manufacturing is orders of magnitude harder than small molecule — flag yield problems early.

2. **Patent + IP Value**: "How strong is the IP protection and what does it mean for valuation?"
   - Load patent-analyzer to map the patent estate — composition of matter, method of use, formulation, and expiry dates with potential extensions
   - Load ip-valuation to translate patent strength into valuation impact — years of exclusivity, erosion curve assumptions, and impact on rNPV
   - Synthesize: A strong composition of matter patent with 12+ years of remaining life is qualitatively different from a method-of-use-only estate expiring in 6 years. IP strength directly modifies the revenue tail in rNPV models.

3. **Full Manufacturing & IP Diligence**: "Complete manufacturing and IP assessment for this asset"
   - Load modality-manufacturing for baseline modality considerations
   - Load cmc-risk-assessor for program-specific CMC risk
   - Load patent-analyzer for IP landscape
   - Load ip-valuation for IP impact on asset value
   - Manufacturing and IP risks are often independent — assess them in parallel, then integrate for the overall pillar score

## Curriculum Order

1. **modality-manufacturing** — Foundation. Before assessing CMC risk for any specific program, understand the manufacturing landscape for the modality. Small molecules, biologics, ADCs, gene therapies, cell therapies, mRNA, and oligonucleotides each have fundamentally different manufacturing challenges, cost structures, and scalability profiles.
2. **cmc-risk-assessor** — Second. With modality context, learn to assess program-specific CMC risk. Evaluate process development maturity, analytical method validation, formulation stability, and regulatory readiness.
3. **ip-valuation** — Third. Before analyzing specific patents, understand how IP translates to value. Learn exclusivity periods, erosion curves, and the valuation impact of different IP strategies.
4. **patent-analyzer** — Fourth. With IP valuation context, learn to analyze specific patent estates. Map composition of matter vs method of use, assess paragraph IV vulnerability, evaluate freedom-to-operate, and estimate effective patent life with adjustments and extensions.

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|------------|--------|
| CMC-risk-assessor flags high manufacturing risk but ip-valuation shows strong IP protection | Both risks stand independently — strong IP does not mitigate manufacturing risk and vice versa | Manufacturing failure means the product cannot be made at commercial scale regardless of IP protection. IP weakness means value erodes to generics regardless of manufacturing capability. These are orthogonal risks. |
| Patent-analyzer shows weak composition of matter patents but modality-manufacturing indicates high barriers to biosimilar entry (e.g., complex biologics) | Acknowledge both — weak patents are a real risk but manufacturing complexity provides a practical moat | Manufacturing complexity is a de facto barrier to entry but not a substitute for IP protection. Complex biologics face biosimilar competition eventually, just on a longer timeline than small molecules. Adjust the erosion curve, do not eliminate it. |
| Modality-manufacturing suggests high COGS but ip-valuation shows long exclusivity enabling premium pricing | Both are inputs to the margin model — high COGS with premium pricing may still yield attractive margins, but COGS trajectory matters | If COGS decline with manufacturing learning curves and scale, initial high COGS may be acceptable. If COGS are structurally high (e.g., autologous cell therapy), even premium pricing may not produce attractive margins at scale. |

## Scope Boundaries

**This director handles**: All questions about CMC risk, manufacturing feasibility, modality-specific manufacturing, COGS estimation, process scalability, patent landscape analysis, freedom-to-operate, IP valuation, regulatory exclusivity, biosimilar/generic erosion, and the intersection of manufacturing and IP for biotech asset diligence.

**Route to Asclepius when**:
- The question involves CMC regulatory risk that requires pathway analysis (route to regulatory-strategy)
- The question involves manufacturing cost inputs to rNPV models (route to asset-valuation)
- The question involves manufacturing differentiation as a competitive advantage (route to competitive-intelligence)
- The question involves manufacturing timeline impact on clinical development (route to clinical-development)
- The question spans multiple diligence pillars and needs orchestrator-level coordination

## Cross-Domain Connections

- **Biotech-venture/cmc-risk-assessor, modality-manufacturing, patent-analyzer, ip-valuation**: Child skills that execute specialist manufacturing and IP analyses
- **Investing/tail-risk**: CMC failure is a tail risk in drug development — manufacturing deficiencies account for a meaningful fraction of Complete Response Letters and can destroy late-stage program value
- **Biotech-venture/cost-estimator**: Manufacturing complexity drives COGS and development costs, which are critical inputs to the rNPV model
