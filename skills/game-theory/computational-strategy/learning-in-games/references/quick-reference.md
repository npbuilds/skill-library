# Learning In Games — Quick Reference


## Independent Learning vs. Centralized Training

| Approach | Description | Convergence | Scalability |
|----------|-------------|-------------|-------------|
| **Independent learners** | Each agent learns independently, treating others as part of the environment | Not guaranteed (non-stationarity) | High |
| **Centralized training, decentralized execution (CTDE)** | A central trainer coordinates learning; at deployment, each agent acts independently | Better convergence guarantees | Medium |
| **Fully centralized** | Joint policy optimization | Best convergence | Low (exponential in # agents) |
