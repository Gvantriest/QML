# ME44207 Quantitative Methods for Logistics – Group Assignment Q2 (Group 2)

Electric vehicle routing with time windows under range uncertainty, solved with Gurobi.

## Setup

```bash
git clone <repository url>
cd qml-assignment-group2
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python check_setup.py
```

`check_setup.py` tells you whether the packages, the Gurobi licence and the data files are in
place. The licence that comes with `pip install gurobipy` is limited to 2000 variables and
constraints; install the free academic licence from gurobi.com for the larger models.

## Layout

| Path | Contents |
| --- | --- |
| `data/` | The three input files, unchanged. Do not edit them. |
| `src/common.py` | Shared helpers: reading data, distances, printing, plotting |
| `src/part1b.py` | Part 1b: deterministic range |
| `src/part2b.py` | Part 2b: chance constraint |
| `src/part3bc.py` | Parts 3b and 3c: emergency charging |
| `src/part3d.py` | Part 3d: our own recourse strategy |
| `output/` | Figures and tables written by the scripts (not tracked by git) |

All source files are stubs with a short description of what the part must produce. Check the
description against the assignment PDF before you start.

Run a part from the repository root:

```bash
python src/part1b.py
```

## Rules from the assignment

- Packages: `numpy`, `pandas`, `math`, `scipy`, `matplotlib.pyplot`, plus `gurobipy`.
- Read the data files as they are; create the depot copy or other extra data in code.
- Time limit of 30 minutes per run; report the gap if a run stops at the limit.
- Use of generative AI must be declared in the report, with the prompts.

## Working together

- `main` always runs. Work on a branch per part (`part1b`, `part2b`, ...) and merge with a
  pull request that one other member has read.
- Agree on the function signatures in `src/common.py` first; everyone depends on them.
- Never commit a Gurobi licence file (`gurobi.lic` is in `.gitignore`).
- Commit small and often, with a message that says what changed.

## Who does what

| Part | Owner | Status |
| --- | --- | --- |
| 1a / 1b | | |
| 2a / 2b | | |
| 3a / 3b / 3c | | |
| 3d | | |
| Report | | |
