"""
Run this once after cloning:  python check_setup.py

It checks that the packages import, that Gurobi has a working licence and that the three
data files are where the scripts expect them. It contains no assignment code.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILES = ["geo_data.txt", "geo_data_large.txt", "range_data.txt"]
ok = True

print(f"Python {sys.version.split()[0]}")
for name in ["numpy", "pandas", "scipy", "matplotlib", "gurobipy"]:
    try:
        module = __import__(name)
        print(f"  ok      {name} {getattr(module, '__version__', '')}")
    except ImportError:
        print(f"  MISSING {name}  ->  pip install -r requirements.txt")
        ok = False

try:
    import gurobipy as gp

    model = gp.Model("licence_check")
    model.Params.OutputFlag = 0
    x = model.addVar(ub=1.0)
    model.setObjective(x, gp.GRB.MAXIMIZE)
    model.optimize()
    print("  ok      Gurobi solved a test model")
    try:
        big = gp.Model("size_check")          # more than the 2000 variables of a restricted licence
        big.Params.OutputFlag = 0
        big.addVars(2500)
        big.optimize()
        print("  ok      full (academic) Gurobi licence")
    except gp.GurobiError:
        print("  WARNING size-limited Gurobi licence: the larger models will not solve. "
              "Install the free academic licence.")
except Exception as error:                     # noqa: BLE001 - report anything that goes wrong
    print(f"  PROBLEM Gurobi: {error}")
    ok = False

for name in DATA_FILES:
    path = os.path.join(HERE, "data", name)
    if os.path.isfile(path):
        with open(path) as handle:
            rows = sum(1 for line in handle if line.strip())
        print(f"  ok      data/{name} ({rows} rows)")
    else:
        print(f"  MISSING data/{name}")
        ok = False

print("\nSetup looks good." if ok else "\nFix the items marked MISSING or PROBLEM above.")
sys.exit(0 if ok else 1)
