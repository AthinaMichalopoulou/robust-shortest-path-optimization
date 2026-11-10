# Mathematical formulation

This document describes the deterministic and robust shortest-path models implemented in the [notebook](../notebooks/robust_shortest_path.ipynb). All models use a directed street network from **Bimhuis** to **Melkweg**, Amsterdam.

## Network, sets, and parameters

| Symbol | Meaning |
| --- | --- |
| $G=(V,E)$ | Directed street network with nodes $V$ and directed edges $E$ |
| $s,t\in V$ | Origin and destination |
| $c_{ij}>0$ | Nominal distance (or travel-time proxy) for directed edge $(i,j)$ |
| $h\in V$ | Congestion hotspot (hotel location) |
| $d(i)$ | Distance from node $i$ to hotspot $h$ |
| $\delta\ge 0$ | Radius of excluded nodes |
| $\alpha_i\ge 0$ | Congestion coefficient at node $i$ |
| $\Gamma\ge 0$ | Total uncertainty budget |

**Decision variable.** $x_{ij}\in\{0,1\}$ indicates whether directed edge $(i,j)$ is used in the chosen route.

For flow balance, define $b_s=1$, $b_t=-1$, and $b_j=0$ for other nodes, and impose

$$
\sum_{i:(j,i)\in E}x_{ji}-\sum_{i:(i,j)\in E}x_{ij}=b_j\qquad\forall j\in V.
$$

The signs follow the baseline model's incoming-minus-outgoing convention as written in the provided notebook; the implementation uses this same convention. In interpreting route direction, the code's network and `get_route` helper determine the displayed path.

## 1. Deterministic shortest path

Minimize nominal distance subject to the shared flow constraints:

$$
\min_x\sum_{(i,j)\in E}c_{ij}x_{ij}.
$$

The binary edge selections and flow conservation encode a network path. The implementation is `shortest_path_model` in [`utils.py`](../utils.py).

## 2. Route with an exclusion radius

Let the forbidden node set be

$$
F(\delta)=\{i\in V:d(i)\le\delta\}.
$$

For each excluded node, forbid all incident selected edges:

$$
\sum_{i:(i,j)\in E}x_{ij}=0,\quad
\sum_{k:(j,k)\in E}x_{jk}=0\qquad\forall j\in F(\delta).
$$

The objective is unchanged. The function `safe_shortest_path_model` adds these restrictions to the deterministic baseline. Larger $\delta$ expands the excluded area and can lengthen the optimal path.

## 3. Robust shortest path with box uncertainty

Congestion changes edge cost to $c_{ij}(1+z_{ij})$, with independent bounded deviations:

$$
\mathcal Z_{\mathrm{box}}=\{z:0\le z_{ij}\le\alpha_i+\alpha_j\ \forall(i,j)\in E\}.
$$

The robust objective minimizes the worst possible total cost:

$$
\min_x\max_{z\in\mathcal Z_{\mathrm{box}}}\sum_{(i,j)\in E}c_{ij}(1+z_{ij})x_{ij}.
$$

Introducing an upper bound $T$ gives

$$
\min_{x,T}T\quad\text{s.t.}\quad
\sum_{(i,j)\in E}c_{ij}(1+z_{ij})x_{ij}\le T\quad\forall z\in\mathcal Z_{\mathrm{box}},
$$

plus flow conservation and binary decision variables. Since $c_{ij}x_{ij}\ge0$ and all deviations are independently bounded, the worst case occurs at their upper bounds, yielding

$$
\min_x\sum_{(i,j)\in E}c_{ij}(1+\alpha_i+\alpha_j)x_{ij}.
$$

The implementation `shortestpath_boxuncertainty` passes these adjusted edge costs to the baseline shortest-path model.

## 4. Robust shortest path with a congestion budget

To avoid assuming that every edge simultaneously reaches its most congested state, use

$$
\mathcal{Z}_{\mathrm{budget}}(\Gamma) = \{ z \mid |z_{ij}| \le \alpha_i + \alpha_j,\quad \sum_{(i,j)\in E}|z_{ij}| \le \Gamma \}.
$$

The objective is to minimize the worst-case value of

$$
\sum_{(i,j)\in E}c_{ij}(1+z_{ij})x_{ij}.
$$

For a fixed $x$, define $d_{ij}=c_{ij}x_{ij}\ge0$ and $\rho_{ij}=\alpha_i+\alpha_j$. Because the uncertain term is maximized and $d_{ij}\ge0$, a worst-case solution may take $z_{ij}\ge0$; negative deviations cannot increase the objective. The inner optimization is therefore equivalent to

$$
\max_z\ \sum_{(i,j)\in E}d_{ij}z_{ij}
\quad\text{s.t. }0\le z_{ij}\le\rho_{ij},\quad\sum_{(i,j)\in E}z_{ij}\le\Gamma.
$$

Its linear-programming dual is

$$
\min_{\lambda,q}\ \Gamma\lambda+\sum_{(i,j)\in E}\rho_{ij}q_{ij}
$$

subject to

$$
\lambda+q_{ij}\ge d_{ij}\quad\forall(i,j)\in E,\qquad\lambda\ge0,\ q_{ij}\ge0.
$$

The deterministic mixed-integer robust counterpart is

$$
\min_{x,T,\lambda,q}\ T
$$

subject to flow balance, binary edge choices, and

$$
\sum_{(i,j)\in E}c_{ij}x_{ij}+\Gamma\lambda+\sum_{(i,j)\in E}(\alpha_i+\alpha_j)q_{ij}\le T,
$$

$$
\lambda+q_{ij}\ge c_{ij}x_{ij}\quad\forall(i,j)\in E,\quad\lambda,q\ge0.
$$

This is the structure used in `shortest_path_budgetuncertainty`. Here $\Gamma$ limits the **sum of absolute congestion deviations**; it does not literally count the number of congested edges.

## Interpretation

The deterministic model minimizes nominal route distance. The exclusion model adds a geographical feasibility constraint. Box and budgeted robust models instead change the objective to account for adverse travel conditions. Their objective values should be compared as *modeled costs*, not automatically as physical route lengths.
