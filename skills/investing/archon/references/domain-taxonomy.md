# Domain Taxonomy — The Investing Skill Map

## Architecture Overview

```
THE ARCHON (orchestrator)
│
├── ① REGIME INTELLIGENCE (director)
│   ├── macro-cycles (knowledge)
│   ├── monetary-regime (knowledge)
│   └── fiscal-regime (knowledge)
│
├── ② REFLEXIVITY & SENTIMENT (director)
│   ├── reflexivity-theory (knowledge)
│   ├── market-psychology (knowledge)
│   └── sentiment-signals (knowledge)
│
├── ③ VALUE & QUALITY (director)
│   ├── intrinsic-value (knowledge)
│   ├── second-level-thinking (knowledge)
│   └── quality-compounders (knowledge)
│
├── ④ RISK ARCHITECTURE (director)
│   ├── position-sizing (knowledge)
│   ├── tail-risk (knowledge)
│   ├── correlation-regimes (knowledge)
│   └── drawdown-psychology (knowledge)
│
├── ⑤ MARKET MICROSTRUCTURE (director)
│   ├── passive-flow-dynamics (knowledge)
│   ├── options-mechanics (knowledge)
│   └── liquidity-topology (knowledge)
│
├── ⑥ ASSET UNIVERSE (director)
│   ├── equities (knowledge)
│   ├── fixed-income (knowledge)
│   ├── commodities (knowledge)
│   ├── currencies (knowledge)
│   ├── digital-assets (knowledge)
│   └── alternatives (knowledge)
│
├── ⑦ GEOPOLITICAL OVERLAY (director)
│   ├── great-power-dynamics (knowledge)
│   ├── energy-security (knowledge)
│   └── secular-themes (knowledge)
│
├── ⑧ SPECIAL SITUATIONS (director)
│   ├── spinoffs-restructuring (knowledge)
│   ├── insider-signals (knowledge)
│   ├── complexity-premium (knowledge)
│   └── event-driven (knowledge)
│
├── ⑨ PORTFOLIO CONSTRUCTION (director)
│   ├── asset-allocation (knowledge)
│   ├── factor-exposure (knowledge)
│   ├── hedging-architecture (knowledge)
│   └── tax-optimization (knowledge)
│
└── ⑩ ADAPTIVE MONITORING (director)
    ├── performance-attribution (knowledge)
    ├── rebalancing-logic (knowledge)
    └── alt-data-monitoring (knowledge)
```

## Subdomain Descriptions

### ① Regime Intelligence
**Purpose:** Answer "what world are we in?" before any other analysis.
**Scope:** Business cycles, credit cycles, monetary policy, fiscal policy, regime classification.
**Key output:** A regime classification that all other subdomains receive as context.

### ② Reflexivity & Sentiment
**Purpose:** Understand what the crowd believes and where feedback loops exist.
**Scope:** Soros's reflexivity theory, behavioral finance, quantitative sentiment, narrative lifecycle analysis.
**Key output:** A consensus map and reflexivity assessment that identifies where prices are shaping fundamentals.

### ③ Value & Quality
**Purpose:** Determine what something is actually worth, independent of market narrative.
**Scope:** DCF and intrinsic value analysis, moat assessment, quality compounding, second-level contrarian thinking.
**Key output:** A valuation with margin of safety assessment and explicit disagreement with consensus (if any).

### ④ Risk Architecture
**Purpose:** Ensure survival. No opportunity justifies catastrophic risk.
**Scope:** Position sizing (Kelly and variants), tail risk management, correlation regime analysis, drawdown psychology.
**Key output:** Position size recommendation, stop-loss level, tail-risk hedge specification, and portfolio stress test results.

### ⑤ Market Microstructure
**Purpose:** Understand how the plumbing of modern markets affects prices.
**Scope:** Passive/ETF flow dynamics, 0DTE options and gamma mechanics, liquidity topology, dark pools.
**Key output:** Structural overlay that identifies when market mechanics (not fundamentals) are driving prices.

### ⑥ Asset Universe
**Purpose:** Provide deep expertise within each asset class.
**Scope:** Equities (factors, sectors, geography), fixed income (rates, credit, duration), commodities (supply/demand), currencies (FX regimes), digital assets (crypto frameworks), alternatives (private markets).
**Key output:** Asset-class-specific opportunity assessment within the current regime context.

### ⑦ Geopolitical Overlay
**Purpose:** Map structural forces that transcend traditional market analysis.
**Scope:** US-China dynamics, energy security and transition, secular themes (AI, demographics, deglobalization, debt).
**Key output:** Geopolitical risk assessment and secular theme conviction levels that modify asset class views.

### ⑧ Special Situations
**Purpose:** Find opportunities in places where institutional investors can't or won't look.
**Scope:** Spinoffs and restructurings, insider buying patterns, complexity premium (holding company discounts, stubs), event-driven (merger arb, activism).
**Key output:** Specific special situation opportunities with catalyst identification and timeline.

### ⑨ Portfolio Construction
**Purpose:** Translate analysis into an actual portfolio.
**Scope:** Strategic and tactical asset allocation, factor exposure management, hedging strategy, tax optimization.
**Key output:** A concrete portfolio allocation with hedges, factor exposures, and tax-aware implementation.

### ⑩ Adaptive Monitoring
**Purpose:** Continuously validate that the thesis is intact and the portfolio is performing as expected.
**Scope:** Performance attribution, rebalancing triggers, alternative data monitoring for early signals.
**Key output:** Thesis validation status, rebalancing recommendations, and early warning signals.

## Cross-Subdomain Dependencies

| Subdomain | Depends On | Feeds Into |
|-----------|-----------|------------|
| Regime Intelligence | (independent — runs first) | Everything else |
| Reflexivity & Sentiment | Regime Intelligence | Value & Quality, Portfolio Construction |
| Value & Quality | Regime Intelligence, Reflexivity & Sentiment | Risk Architecture, Portfolio Construction |
| Risk Architecture | Regime Intelligence, Value & Quality | Portfolio Construction |
| Market Microstructure | (semi-independent) | Risk Architecture, Portfolio Construction |
| Asset Universe | Regime Intelligence, Geopolitical Overlay | Value & Quality, Portfolio Construction |
| Geopolitical Overlay | (semi-independent) | Asset Universe, Regime Intelligence |
| Special Situations | (semi-independent) | Value & Quality, Risk Architecture |
| Portfolio Construction | All of the above | Adaptive Monitoring |
| Adaptive Monitoring | Portfolio Construction | Regime Intelligence (loop back) |
