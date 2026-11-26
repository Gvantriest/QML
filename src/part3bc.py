"""
Part 3b and 3c - two-stage stochastic model with emergency charging

First stage: routes. Second stage: emergency charges per vehicle and monthly scenario
(12 equally likely scenarios), each with a fixed penalty.
3b: default data, with and without time windows, 3 penalty values that lead to different
    routing decisions. Report: first-stage routes, total distance, vehicles used,
    occurrence of emergency charging and its penalty, computational time. Compare with
    Parts 1b and 2b.
3c: data/geo_data_large.txt, time-window case, same penalty values; adjust the number of
    vehicles. Compare with 3b.

Run from the repository root:  python src/part3bc.py
"""
import common


def build_model():
    """Build the Gurobi model of this part (see the formulation in the report)."""
    raise NotImplementedError("TODO")


def run_experiments():
    """Solve every experiment of this part, print the results and save the plots."""
    raise NotImplementedError("TODO")


if __name__ == "__main__":
    run_experiments()
