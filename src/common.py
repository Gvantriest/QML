"""
Shared helpers for all parts: data, distances, reporting, plotting.

Everything here is a stub. Agree on the function signatures first, so that the part
scripts can be written in parallel.

Allowed packages: numpy, pandas, math, scipy, matplotlib.pyplot (and gurobipy).
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
OUTPUT_DIR = os.path.join(ROOT, "output")

GEO_FILE = os.path.join(DATA_DIR, "geo_data.txt")
GEO_FILE_LARGE = os.path.join(DATA_DIR, "geo_data_large.txt")
RANGE_FILE = os.path.join(DATA_DIR, "range_data.txt")

TIME_LIMIT = 1800   # seconds; the assignment allows 30 minutes per run


def read_locations(path):
    """
    Read a location file AS IS (no header, whitespace separated).
    Columns: LOC_ID, XCOORD, YCOORD, READYTIME, DUETIME, SERVICETIME. Row 0 is the depot.
    """
    raise NotImplementedError("TODO")


def read_ranges(path):
    """Read the monthly range scenarios AS IS. Columns: MONTH, RANGE."""
    raise NotImplementedError("TODO")


def distance_matrix(locations):
    """Euclidean distance between every pair of nodes (distance = travel time)."""
    raise NotImplementedError("TODO")


def extract_routes(x_values):
    """Turn the solved arc variables into one ordered list of nodes per vehicle."""
    raise NotImplementedError("TODO")


def print_solution(title, routes, runtime):
    """
    Print what the assignment asks for per experiment: total distance, route per vehicle,
    number of vehicles used, remaining range and visit time at each location, run time.
    """
    raise NotImplementedError("TODO")


def plot_routes(locations, routes, title, filename):
    """2D plot of the routes of all vehicles, saved in OUTPUT_DIR."""
    raise NotImplementedError("TODO")
