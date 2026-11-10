# Results and interpretation

This page compares the routes and objective values obtained from the deterministic, crowd-avoidance, and robust shortest-path models on the Amsterdam network. It also summarizes how the solutions respond to the avoidance radius $\delta$ and congestion budget $\Gamma$.

## Deterministic benchmark and model comparison

| Model | Parameter | Reported objective | Interpretation |
| --- | --- | ---: | --- |
| Nominal shortest path | — | 3,352.59 | Nominal route distance (m) |
| Exclusion model | $\delta=250$ m | 3,424.36 | Nominal route distance (m) |
| Box uncertainty | Independent edge upper bounds | 4,849.18 | Congestion-adjusted worst-case cost |
| Budget uncertainty | $\Gamma=5$ | 3,967.22 | Congestion-adjusted worst-case cost |

The exclusion model sacrifices a small amount of nominal distance to avoid the restricted area. The box model penalizes every edge according to its largest permitted congestion factor, while the budget model limits the total congestion deviation. **The robust objective values are not physical route lengths**, so a larger value does not alone show that the chosen physical path is proportionally longer.

## Avoidance-radius sensitivity

| $\delta$ (m) | Optimal nominal path length (m) |
| ---: | ---: |
| 0 | 3,353.89 |
| 50 | 3,421.70 |
| 250 | 3,424.36 |
| 450 | 3,426.82 |
| 650 | 3,508.26 |
| 850 | 3,755.30 |
| 1,050 | approximately 4,080 |

Route lengths are non-decreasing as the excluded area expands. The stronger detours at larger radii show the cost of strict geographic avoidance. Note that $\delta=0$ still excludes the hotspot node itself, so this is not exactly the same feasible problem as the unrestricted deterministic benchmark.

## Budget-uncertainty sensitivity

| $\Gamma$ | Worst-case objective |
| ---: | ---: |
| 0 | 3,352.59 |
| 1 | 3,541.17 |
| 2 | 3,670.86 |
| 3 | 3,784.10 |
| 4 | 3,892.52 |
| 5 | 3,967.22 |

The worst-case cost increases with the uncertainty budget. At $\Gamma=0$, it matches the deterministic objective. The resulting route was reported to remain essentially unchanged across the tested budgets, suggesting that its nominally optimal edges also performed competitively under this form of budgeted uncertainty.

## Takeaways

- **Geographic avoidance** offers direct control over where a route may pass, at the expense of longer nominal distance.
- **Box uncertainty** protects against a highly conservative simultaneous congestion scenario.
- **Budgeted uncertainty** allows a more adjustable trade-off between nominal efficiency and worst-case protection.

The notebook contains route plots for each scenario, allowing the geographical outcomes to be inspected alongside these numerical summaries.
