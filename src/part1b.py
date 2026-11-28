"""
Part 1b - VRP with time windows and a deterministic range

Settings: default data (data/geo_data.txt), 3 vehicles, range = mean of the monthly ranges.
Experiments: with and without time windows.
Report per experiment: total distance, route of each vehicle, remaining range and visit
time at each location, a 2D plot of the routes, computational time.

Run from the repository root:  python src/part1b.py
"""
import common


def run_experiments():
    locations = common.read_locations(common.GEO_FILE)
    ranges = common.read_ranges(common.RANGE_FILE)
    R = ranges["RANGE"].mean()                # R = mean(RANGE)

    common.solve_and_report(locations, R, True, "Part 1b - with time windows",
                            "part1b_with_tw.png")
    common.solve_and_report(locations, R, False, "Part 1b - without time windows",
                            "part1b_without_tw.png")


if __name__ == "__main__":
    run_experiments()
