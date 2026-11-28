"""
Shared code for Parts 1b and 2b: data, the routing model, printing and plotting.

The model follows our formulation "Assignment 1a QML" constraint by constraint; the numbers
in the comments, (1) to (20), are the equation numbers of that document. Part 2 uses the
same model with another right-hand side in (6).

Allowed packages: numpy, pandas, math, scipy, matplotlib.pyplot (and gurobipy).
"""
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gurobipy as gp
from gurobipy import GRB

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
OUTPUT_DIR = os.path.join(ROOT, "output")

GEO_FILE = os.path.join(DATA_DIR, "geo_data.txt")
GEO_FILE_LARGE = os.path.join(DATA_DIR, "geo_data_large.txt")
RANGE_FILE = os.path.join(DATA_DIR, "range_data.txt")

TIME_LIMIT = 1800   # seconds; the assignment allows 30 minutes per run
N_VEHICLES = 3


# ------------------------------------------------------------------------------------
# Data
# ------------------------------------------------------------------------------------
def read_locations(path):
    """
    Read a location file AS IS (no header, whitespace separated).
    Columns: LOC_ID, XCOORD, YCOORD, READYTIME, DUETIME, SERVICETIME. Row 0 is the depot.
    """
    columns = ["LOC_ID", "XCOORD", "YCOORD", "READYTIME", "DUETIME", "SERVICETIME"]
    return pd.read_csv(path, sep=r"\s+", header=None, names=columns)


def read_ranges(path):
    """Read the monthly range scenarios AS IS. Columns: MONTH, RANGE."""
    return pd.read_csv(path, sep=r"\s+", header=None, names=["MONTH", "RANGE"])


def distance_matrix(locations):
    """Euclidean distance C[i, j] between every pair of nodes (distance = travel time)."""
    x = locations["XCOORD"].to_numpy(dtype=float)
    y = locations["YCOORD"].to_numpy(dtype=float)
    return np.sqrt((x[:, None] - x[None, :]) ** 2 + (y[:, None] - y[None, :]) ** 2)


# ------------------------------------------------------------------------------------
# Model (formulation of Assignment 1a; Part 2a only changes max_range)
# ------------------------------------------------------------------------------------
def build_model(locations, n_vehicles, max_range, time_windows=True):
    """
    Build the routing model.
      max_range    : right-hand side of (6): R in Part 1, R_min,alpha in Part 2
      time_windows : False = case "without time windows". The pickups then get the window
                     of the depot, so only the opening hours of the depot remain.
    Returns the model and the variables x, z, u, t.
    """
    N = list(range(len(locations)))          # nodes, 0 = depot
    customers = N[1:]                         # N \ {0}
    V = list(range(n_vehicles))               # vehicles

    C = distance_matrix(locations)
    T_r = locations["READYTIME"].to_numpy(dtype=float).copy()
    T_d = locations["DUETIME"].to_numpy(dtype=float).copy()
    T_s = locations["SERVICETIME"].to_numpy(dtype=float)
    if not time_windows:
        T_r[1:] = T_r[0]
        T_d[1:] = T_d[0]

    M_N = len(N)                              # big-M, M_N >= |N|
    M_T = T_d.max()                           # big-M, M_T >= max T_d

    model = gp.Model("VRPTW")

    # decision variables, (17) - (20)
    x = model.addVars(N, N, V, vtype=GRB.BINARY, name="x")   # vehicle v drives from i to j
    z = model.addVars(N, V, vtype=GRB.BINARY, name="z")      # node i is assigned to vehicle v
    u = model.addVars(N, V, lb=0.0, name="u")                # visit order of node i for vehicle v
    t = model.addVars(N, V, lb=0.0, name="t")                # start of service at node i for vehicle v

    # (1) minimise the total distance
    model.setObjective(gp.quicksum(C[i, j] * x[i, j, v] for i in N for j in N for v in V),
                       GRB.MINIMIZE)

    # (2) every pickup location is assigned to exactly one vehicle
    for i in customers:
        model.addConstr(gp.quicksum(z[i, v] for v in V) == 1, name=f"c2[{i}]")

    for v in V:
        # (3) a vehicle that serves a pickup location also uses the depot
        model.addConstr(gp.quicksum(z[j, v] for j in customers) <= (M_N - 1) * z[0, v],
                        name=f"c3[{v}]")
        # (4) one arc out of every node of the route, (5) one arc into every node of the route
        for i in N:
            model.addConstr(gp.quicksum(x[i, j, v] for j in N) == z[i, v], name=f"c4[{i},{v}]")
        for j in N:
            model.addConstr(gp.quicksum(x[i, j, v] for i in N) == z[j, v], name=f"c5[{j},{v}]")
        # (6) range of the vehicle
        model.addConstr(gp.quicksum(C[i, j] * x[i, j, v] for i in N for j in N) <= max_range,
                        name=f"c6[{v}]")

        # --- subtour elimination ---
        # (7) the visit order increases along a driven arc
        for i in customers:
            for j in customers:
                if i != j:
                    model.addConstr(u[i, v] - u[j, v] + (M_N + 1) * x[i, j, v] <= M_N,
                                    name=f"c7[{i},{j},{v}]")
        # (8) the depot is the first node of a used vehicle
        model.addConstr(u[0, v] == z[0, v], name=f"c8[{v}]")
        for i in customers:
            # (9) no visit order for nodes that are not on the route
            model.addConstr(u[i, v] <= M_N * z[i, v], name=f"c9[{i},{v}]")
            # (10) the visit order is at most the number of nodes on the route
            model.addConstr(gp.quicksum(z[j, v] for j in N) - u[i, v] >= 0, name=f"c10[{i},{v}]")
            # (11) pickup locations come after the depot
            model.addConstr(u[i, v] >= 2 * z[i, v], name=f"c11[{i},{v}]")
        # (12) no arc from a node to itself
        for i in N:
            model.addConstr(x[i, i, v] == 0, name=f"c12[{i},{v}]")

        # --- time ---
        for j in N:
            # (13) a vehicle cannot be at j before it has driven there from the depot
            model.addConstr(t[j, v] >= (T_r[0] + C[0, j]) * z[j, v], name=f"c13[{j},{v}]")
        for i in customers:
            # (14) not before the ready time
            model.addConstr(t[i, v] >= T_r[i] * z[i, v], name=f"c14[{i},{v}]")
        for i in N:
            # (15) not after the due time (for the depot: back before closing time)
            model.addConstr(t[i, v] <= T_d[i] * z[i, v], name=f"c15[{i},{v}]")
        # (16) service at i and the drive to j must be finished before the start at j
        #      (j = 0 is the return to the depot)
        for i in customers:
            for j in N:
                if i != j:
                    model.addConstr(t[i, v] - t[j, v] + (M_T + T_s[i] + C[i, j]) * x[i, j, v] <= M_T,
                                    name=f"c16[{i},{j},{v}]")

    model.Params.TimeLimit = TIME_LIMIT
    model.Params.OutputFlag = 0               # set to 1 to see the Gurobi log
    return model, x, z, u, t


# ------------------------------------------------------------------------------------
# Results
# ------------------------------------------------------------------------------------
def extract_routes(x, n_nodes, n_vehicles):
    """Follow the arcs of every vehicle from the depot: {vehicle: [0, ..., 0]} ([] = not used)."""
    routes = {}
    for v in range(n_vehicles):
        successor = {i: j for i in range(n_nodes) for j in range(n_nodes) if x[i, j, v].X > 0.5}
        route = []
        if 0 in successor:
            route = [0]
            node = successor[0]
            while node != 0:
                route.append(node)
                node = successor[node]
            route.append(0)
        routes[v] = route
    return routes


def print_solution(title, locations, routes, t, max_range, runtime, gap):
    """Print the results the assignment asks for; returns the total distance."""
    C = distance_matrix(locations)
    total = sum(C[i, j] for route in routes.values() for i, j in zip(route[:-1], route[1:]))
    used = sum(1 for route in routes.values() if route)

    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)
    print(f"Total distance     : {total:.2f}")
    print(f"Vehicles used      : {used} of {len(routes)}")
    print(f"Range per vehicle  : {max_range:.2f}")
    print(f"Computational time : {runtime:.2f} s (gap {100 * gap:.2f} %)")

    for v, route in routes.items():
        if not route:
            print(f"\nVehicle {v + 1}: not used")
            continue
        length = sum(C[i, j] for i, j in zip(route[:-1], route[1:]))
        print(f"\nVehicle {v + 1}: {' - '.join(str(i) for i in route)}   (distance {length:.2f})")
        print(f"  {'location':>8} {'visit time':>11} {'distance driven':>16} {'remaining range':>16}")
        driven = 0.0
        previous = 0
        for i in route[1:]:
            driven += C[previous, i]
            name = "depot" if i == 0 else str(i)
            print(f"  {name:>8} {t[i, v].X:>11.2f} {driven:>16.2f} {max_range - driven:>16.2f}")
            previous = i
    return total


def plot_routes(locations, routes, title, filename):
    """2D plot of the routes of all vehicles, saved in OUTPUT_DIR."""
    xs = locations["XCOORD"].to_numpy(dtype=float)
    ys = locations["YCOORD"].to_numpy(dtype=float)
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown"]
    styles = ["-", "--", "-.", ":"]

    fig, ax = plt.subplots(figsize=(6, 6))
    for v, route in routes.items():
        if route:
            ax.plot(xs[route], ys[route], color=colors[v % len(colors)],
                    linestyle=styles[v % len(styles)], linewidth=2, label=f"Vehicle {v + 1}")
    ax.scatter(xs[1:], ys[1:], color="white", edgecolor="black", zorder=3)
    ax.scatter(xs[0], ys[0], color="black", marker="s", s=80, zorder=3)
    ax.annotate("depot", (xs[0], ys[0]), textcoords="offset points", xytext=(6, -12))
    for i in range(1, len(locations)):
        ax.annotate(str(i), (xs[i], ys[i]), textcoords="offset points", xytext=(6, 6))
    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.legend()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"\nPlot saved: {path}")


def solve_and_report(locations, max_range, time_windows, title, filename, n_vehicles=N_VEHICLES):
    """Build, solve, print and plot one experiment. Returns the total distance or None."""
    model, x, z, u, t = build_model(locations, n_vehicles, max_range, time_windows)
    model.optimize()

    if model.SolCount == 0:
        reason = "infeasible" if model.Status == GRB.INFEASIBLE else "no solution found in time"
        print("\n" + "=" * 78)
        print(title)
        print("=" * 78)
        print(f"No solution: {reason} with {n_vehicles} vehicles and range {max_range:.2f} "
              f"({model.Runtime:.2f} s)")
        return None

    routes = extract_routes(x, len(locations), n_vehicles)
    total = print_solution(title, locations, routes, t, max_range, model.Runtime, model.MIPGap)
    plot_routes(locations, routes, f"{title}\ntotal distance {total:.2f}", filename)
    return total
