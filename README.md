# Robust Shortest-Path Optimization under Urban Congestion

**Deterministic routing · Crowd avoidance · Robust optimization under uncertain congestion**

## Project overview

Choosing a route through a city involves more than minimizing distance. Crowded locations can make an otherwise short route less desirable, and uncertainty about congestion can complicate decisions before a journey begins.

This project studies **shortest-path optimization under urban congestion** using an Amsterdam street network and a journey from **Bimhuis to Melkweg**. It compares a conventional shortest path with approaches that explicitly avoid crowded areas or account for uncertainty in travel costs. The models are implemented in **Python with Pyomo**.

## The routing problem

The street network consists of intersections connected by road segments. The objective is to select a continuous route between a specified origin and destination while considering the trade-off between direct travel and exposure to congestion.

A shortest route under nominal conditions may pass close to a crowded hotspot. Avoiding that area requires a detour, while planning against uncertain congestion requires choosing a route that remains preferable even when conditions deteriorate. The central question is **how the optimal route changes as congestion restrictions and uncertainty assumptions become more conservative**.

The project investigates this question through a deterministic reference and three related optimization approaches.

## Optimization models

### 1. Deterministic shortest-path benchmark

A shortest-path model identifies the route with the minimum total nominal distance. It provides a reference against which the congestion-aware alternatives can be compared.

### 2. Crowd-avoidant routing

The model excludes intersections within a specified distance of a congestion hotspot. An **exclusion radius** controls how much of the surrounding area the route must avoid.

A sensitivity analysis examines how different exclusion radii affect the selected path and the additional distance required to avoid the hotspot.

### 3. Robust shortest path with interval uncertainty

The robust model represents congestion-related travel costs as uncertain values within prescribed intervals. It selects a path while accounting for the worst-case costs permitted by those intervals.

This approach shows what happens when the route must remain protected against adverse congestion on all selected edges simultaneously.

### 4. Robust shortest path with budgeted uncertainty

The budgeted model limits how much congestion can simultaneously deviate from nominal conditions. An **uncertainty budget** controls the level of conservatism, allowing the analysis to explore alternatives between nominal routing and more protective route choices.

The project compares solutions under different uncertainty budgets to investigate their influence on the routing objective and path selection.

## Results and observations

| Approach | Setting | Reported objective |
| --- | --- | ---: |
| Deterministic shortest path | Nominal conditions | 3,352.59 m |
| Crowd-avoidant routing | Exclusion radius of 250 m | 3,424.36 m |
| Interval-robust routing | Full interval uncertainty | 4,849.18 (adjusted cost) |
| Budgeted robust routing | Uncertainty budget of 5 | 3,967.22 (worst-case cost) |

The crowd-avoidant path is longer than the deterministic shortest route because it must stay clear of the hotspot. The robust models instead balance nominal travel cost against uncertain congestion. **Their adjusted objective values are not directly comparable with the physical distances reported for the first two models.**

The sensitivity analyses illustrate how larger exclusion regions increase the required detour, while larger uncertainty budgets make the robust objective more conservative.

## Project files

- [Mathematical formulation](docs/model_formulation.md): graph notation, decision variables, objectives, constraints, and robust counterparts.
- [Results and interpretation](results/README.md): route comparisons and sensitivity analyses.
- [Optimization notebook](notebooks/robust_shortest_path.ipynb): model implementations, experiments, and route visualizations.
- [Utilities](utils.py): network setup and reusable support functions.

## Tools and reproducibility

The models use **Pyomo** with the **HiGHS** solver. The network and visualization workflows use **OSMnx**, **NumPy**, and **Matplotlib**. The notebook also draws on publicly hosted network helper functions through an external course resource.

Dependencies are listed in [requirements.txt](requirements.txt). The notebook contains the implementations, numerical results, and route figures, while the [results document](results/README.md) provides the fuller interpretation. Reproducing the workflow requires access to the external network helper resources.

## Acknowledgement

This project originated from Mathematical Optimization coursework at **Vrije Universiteit Amsterdam (2025–2026)**. The problem setting and selected utility code were provided in the course materials.
