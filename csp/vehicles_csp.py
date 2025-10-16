"""
CSP: Schedule 5 vehicles (A,B,C,D,E) with time slots {1,2,3,4} and stops {CGI, JB_Hall}.
Each vehicle selects (time, stop, action) where action in {arrive, leave}.

Constraints (formalized):
- B.time = 1 and B.action = arrive
- D.time >= 3
- A.time <= 2
- If D.action = arrive and C.action = leave then D.time < C.time
- A.stop = CGI, B.stop = CGI, C.stop = CGI
- D.stop = JB_Hall, E.stop = JB_Hall
- No two vehicles share the same (time, stop)

Includes a simple backtracking solver and DOT graph string for the constraint graph.
"""
from __future__ import annotations
from typing import Dict, Tuple, List, Optional, Set

Time = int
Stop = str
Action = str
Assignment = Dict[str, Tuple[Time, Stop, Action]]

STOPS = ["CGI", "JB_Hall"]
ACTIONS = ["arrive", "leave"]
TIMES = [1, 2, 3, 4]
VEHICLES = ["A", "B", "C", "D", "E"]

REQUIRED_STOPS = {
    "A": "CGI",
    "B": "CGI",
    "C": "CGI",
    "D": "JB_Hall",
    "E": "JB_Hall",
}


def domain(vehicle: str) -> List[Tuple[Time, Stop, Action]]:
    stop = REQUIRED_STOPS[vehicle]
    vals: List[Tuple[Time, Stop, Action]] = []
    for t in TIMES:
        for a in ACTIONS:
            vals.append((t, stop, a))
    # Apply unary constraints directly
    if vehicle == "B":
        vals = [(1, stop, "arrive")]
    if vehicle == "D":
        vals = [(t, stop, a) for (t, stop, a) in vals if t >= 3]
    if vehicle == "A":
        vals = [(t, stop, a) for (t, stop, a) in vals if t <= 2]
    return vals


def consistent(partial: Assignment) -> bool:
    # No two vehicles share same (time, stop)
    seen: Set[Tuple[Time, Stop]] = set()
    for v, (t, s, a) in partial.items():
        ts = (t, s)
        if ts in seen:
            return False
        seen.add(ts)

    # If both D and C assigned, ensure D arrives before C leaves
    if "D" in partial and "C" in partial:
        tD, sD, aD = partial["D"]
        tC, sC, aC = partial["C"]
        if aD == "arrive" and aC == "leave":
            if not (tD < tC):
                return False
    return True


def backtrack(assign: Assignment, order: List[str]) -> Optional[Assignment]:
    if len(assign) == len(order):
        return assign
    v = order[len(assign)]
    for val in domain(v):
        assign[v] = val
        if consistent(assign):
            result = backtrack(assign, order)
            if result:
                return result
        del assign[v]
    return None


def solve() -> Optional[Assignment]:
    # Heuristic: order vehicles with tightest constraints first
    order = ["B", "D", "A", "C", "E"]
    return backtrack({}, order)


CONSTRAINT_GRAPH_DOT = """
digraph G {
  rankdir=LR;
  A -> B [label="no same (time,stop)"];
  A -> C [label="no same (time,stop)"];
  B -> C [label="no same (time,stop)"];
  D -> E [label="no same (time,stop)"];
  C -> D [label="D.arrive before C.leave"];
}
"""

if __name__ == "__main__":
    solution = solve()
    if solution:
        for v in VEHICLES:
            print(f"{v}: time={solution[v][0]}, stop={solution[v][1]}, action={solution[v][2]}")
    else:
        print("No solution found.")
