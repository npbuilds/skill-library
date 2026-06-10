# Manufacturing Ip — Quick Reference


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

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|------------|--------|
| CMC-risk-assessor flags high manufacturing risk but ip-valuation shows strong IP protection | Both risks stand independently — strong IP does not mitigate manufacturing risk and vice versa | Manufacturing failure means the product cannot be made at commercial scale regardless of IP protection. IP weakness means value erodes to generics regardless of manufacturing capability. These are orthogonal risks. |
| Patent-analyzer shows weak composition of matter patents but modality-manufacturing indicates high barriers to biosimilar entry (e.g., complex biologics) | Acknowledge both — weak patents are a real risk but manufacturing complexity provides a practical moat | Manufacturing complexity is a de facto barrier to entry but not a substitute for IP protection. Complex biologics face biosimilar competition eventually, just on a longer timeline than small molecules. Adjust the erosion curve, do not eliminate it. |
| Modality-manufacturing suggests high COGS but ip-valuation shows long exclusivity enabling premium pricing | Both are inputs to the margin model — high COGS with premium pricing may still yield attractive margins, but COGS trajectory matters | If COGS decline with manufacturing learning curves and scale, initial high COGS may be acceptable. If COGS are structurally high (e.g., autologous cell therapy), even premium pricing may not produce attractive margins at scale. |
