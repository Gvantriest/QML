"""
Part 2b - chance-constrained range

Settings: same data and vehicles as Part 1; range ~ Normal(mu, sigma^2) estimated from
data/range_data.txt. Agree in the group on the estimator of sigma (divide by n or n - 1)
and use the same one in the report.
Experiments: alpha in {0.50, 0.75, 0.90, 0.99}, each with and without time windows.
Report per experiment: total distance, routes, number of vehicles used, remaining range
and visit time at each location, computational time.

Run from the repository root:  python src/part2b.py
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
