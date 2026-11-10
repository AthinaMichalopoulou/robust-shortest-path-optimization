"""Road-network helpers and deterministic shortest-path baseline.

The helper functions and baseline modeling approach originate from the
Mathematical Optimization course materials (VU Amsterdam, 2025–2026):
https://github.com/alessandrozocca/MO2025

The course helper code is imported from its upstream repository; it is not
reproduced or claimed as original code here.
"""

import httpimport
import pyomo.environ as pyo

with httpimport.github_repo("alessandrozocca", "MO2025"):
    from helpers.assignment3 import (
        get_network, make_instance, get_route, get_distances_to,
        get_crowdedness, plot_network, plot_network_heatmap,
    )


def shortest_path_model(s, t, nodes, edges, pred, succ):
    """Construct the deterministic binary network-flow shortest-path model."""
    model = pyo.ConcreteModel("Deterministic Shortest Path")
    model.s = pyo.Param(initialize=s)
    model.t = pyo.Param(initialize=t)
    model.nodes = pyo.Set(initialize=nodes)
    model.edges = pyo.Set(initialize=list(edges.keys()))
    model.x = pyo.Var(model.edges, domain=pyo.Binary)

    @model.Objective()
    def total_distance(m):
        return sum(m.x[i, j] * edges[i, j] for i, j in m.edges)

    @model.Expression(model.nodes)
    def incoming(m, j):
        return sum(m.x[j, i] for i in pred[j])

    @model.Expression(model.nodes)
    def outgoing(m, j):
        return sum(m.x[i, j] for i in succ[j])

    @model.Expression(model.nodes)
    def b(m, j):
        return (j in {s, t}) * (-1) ** (j == t)

    @model.Constraint(model.nodes)
    def flow(m, j):
        return m.incoming[j] - m.outgoing[j] == m.b[j]

    return model
