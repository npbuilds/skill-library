# Population Dynamics — Quick Reference


## Quick Reference

| Protocol | Update Rule | Resulting Dynamics |
|----------|-----------|-------------------|
| **Imitation (proportional)** | Copy a random agent's strategy with probability proportional to their fitness | Replicator dynamics |
| **Best response** | Switch to the current best response to the population | Best response dynamics |
| **Logit (perturbed BR)** | Choose strategies proportional to exp(β × fitness) | Logit dynamics (with noise parameter β) |
| **Smith** | Switch to a better strategy with rate proportional to improvement | Smith dynamics |
| **Pairwise comparison** | Meet a random agent; switch if they're doing better, with probability proportional to the difference | Pairwise comparison dynamics |
