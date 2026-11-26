"""
Part 1b - VRP with time windows and a deterministic range

Settings: default data (data/geo_data.txt), 3 vehicles, range = mean of the monthly ranges.
Experiments: with and without time windows.
Report per experiment: total distance, route of each vehicle, remaining range and visit
time at each location, a 2D plot of the routes, computational time.
Discuss: the two results and their computational times.

Run from the repository root:  python src/part1b.py
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
