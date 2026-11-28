"""
Part 2b - chance-constrained range

Settings: same data and vehicles as Part 1; range ~ Normal(mu, sigma^2) estimated from
data/range_data.txt. As in our formulation of 2a, sigma is the population standard
deviation (divide by |R|) and constraint (6) becomes: route length <= mu - sigma * z_alpha.
Experiments: alpha in {0.50, 0.75, 0.90, 0.99}, each with and without time windows.
Report per experiment: total distance, routes, number of vehicles used, remaining range
and visit time at each location, computational time.

Run from the repository root:  python src/part2b.py
"""
import numpy as np
from scipy.stats import norm

import common

ALPHAS = [0.50, 0.75, 0.90, 0.99]


def run_experiments():
    locations = common.read_locations(common.GEO_FILE)
    ranges = common.read_ranges(common.RANGE_FILE)["RANGE"].to_numpy(dtype=float)

    mu = ranges.mean()
    sigma = np.sqrt(((ranges - mu) ** 2).sum() / len(ranges))
    print(f"mu = {mu:.2f}, sigma = {sigma:.2f}")

    summary = []
    for time_windows in (True, False):
        case = "with time windows" if time_windows else "without time windows"
        for alpha in ALPHAS:
            z_alpha = norm.ppf(alpha)
            R_min = mu - sigma * z_alpha      # R_min,alpha
            total = common.solve_and_report(
                locations, R_min, time_windows, f"Part 2b - alpha = {alpha:.2f}, {case}",
                f"part2b_alpha{alpha:.2f}_{'with' if time_windows else 'without'}_tw.png")
            summary.append((case, alpha, R_min, total))

    print("\n" + "=" * 78)
    print("Summary Part 2b")
    print("=" * 78)
    print(f"{'case':<22} {'alpha':>6} {'range limit':>12} {'total distance':>15}")
    for case, alpha, R_min, total in summary:
        distance = "infeasible" if total is None else f"{total:.2f}"
        print(f"{case:<22} {alpha:>6.2f} {R_min:>12.2f} {distance:>15}")


if __name__ == "__main__":
    run_experiments()
