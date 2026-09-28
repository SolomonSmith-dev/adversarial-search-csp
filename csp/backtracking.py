"""
A small, generic constraint-satisfaction backtracking framework.

This generalizes the ad-hoc backtracking used by the knights and vehicle
solvers into a reusable core with two classic optimizations:

- **MRV (minimum-remaining-values)** variable ordering: always branch on the
  most constrained unassigned variable first, which fails fast.
- **Forward checking**: after each assignment, prune values from the domains of
  neighboring variables that can no longer be consistent, and abandon the
  branch immediately if any domain becomes empty.

Both are toggleable so the effect can be measured (see ``SearchStats``).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Generic, Hashable, List, Optional, Sequence, TypeVar

V = TypeVar("V", bound=Hashable)  # variable type
D = TypeVar("D")                  # domain-value type


class Constraint(Generic[V, D]):
    """A constraint over a subset of variables.

    Subclasses implement ``satisfied``, which must return True when the
    constraint is not yet violated by the (possibly partial) assignment. A
    constraint referencing an unassigned variable should return True, deferring
    its judgment until every variable it touches has a value.
    """

    def __init__(self, variables: Sequence[V]):
        self.variables = list(variables)

    def satisfied(self, assignment: Dict[V, D]) -> bool:
        raise NotImplementedError


@dataclass
class SearchStats:
    """Instrumentation so the value of MRV / forward checking is observable."""
    nodes: int = 0        # variable/value pairs tried
    backtracks: int = 0   # dead ends abandoned
    prunings: int = 0     # domain values removed by forward checking

    def __str__(self) -> str:
        return (f"nodes={self.nodes} backtracks={self.backtracks} "
                f"prunings={self.prunings}")


class CSP(Generic[V, D]):
    def __init__(self, variables: Sequence[V], domains: Dict[V, List[D]]):
        self.variables: List[V] = list(variables)
        self.domains: Dict[V, List[D]] = domains
        self.constraints: Dict[V, List[Constraint[V, D]]] = {v: [] for v in self.variables}
        for v in self.variables:
            if v not in self.domains:
                raise ValueError(f"Variable {v!r} has no domain.")

    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        for v in constraint.variables:
            if v not in self.constraints:
                raise ValueError(f"Constraint references unknown variable {v!r}.")
            self.constraints[v].append(constraint)

    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        """True if no constraint touching ``variable`` is violated."""
        return all(c.satisfied(assignment) for c in self.constraints[variable])


def backtracking_search(
    csp: CSP[V, D],
    use_mrv: bool = True,
    use_forward_checking: bool = True,
) -> tuple[Optional[Dict[V, D]], SearchStats]:
    """Solve ``csp`` and return (assignment or None, search statistics)."""
    stats = SearchStats()

    def select_unassigned(assignment: Dict[V, D], domains: Dict[V, List[D]]) -> V:
        unassigned = [v for v in csp.variables if v not in assignment]
        if use_mrv:
            # Fewest legal values remaining -> branch here first.
            return min(unassigned, key=lambda v: len(domains[v]))
        return unassigned[0]

    def forward_check(
        variable: V, value: D, domains: Dict[V, List[D]], assignment: Dict[V, D]
    ) -> Optional[Dict[V, List[D]]]:
        """Prune neighbor domains; return new domains, or None on wipeout."""
        pruned = {v: list(vals) for v, vals in domains.items()}
        pruned[variable] = [value]
        for constraint in csp.constraints[variable]:
            for other in constraint.variables:
                if other in assignment:
                    continue
                surviving = []
                for candidate in pruned[other]:
                    trial = dict(assignment)
                    trial[other] = candidate
                    if constraint.satisfied(trial):
                        surviving.append(candidate)
                    else:
                        stats.prunings += 1
                pruned[other] = surviving
                if not surviving:
                    return None
        return pruned

    def backtrack(assignment: Dict[V, D], domains: Dict[V, List[D]]) -> Optional[Dict[V, D]]:
        if len(assignment) == len(csp.variables):
            return dict(assignment)
        variable = select_unassigned(assignment, domains)
        for value in domains[variable]:
            stats.nodes += 1
            local = dict(assignment)
            local[variable] = value
            if not csp.consistent(variable, local):
                continue
            next_domains = domains
            if use_forward_checking:
                next_domains = forward_check(variable, value, domains, local)
                if next_domains is None:
                    stats.backtracks += 1
                    continue
            result = backtrack(local, next_domains)
            if result is not None:
                return result
            stats.backtracks += 1
        return None

    initial = {v: list(csp.domains[v]) for v in csp.variables}
    solution = backtrack({}, initial)
    return solution, stats
