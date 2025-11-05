import sys
from collections import deque, defaultdict
from typing import List, Tuple

def solve(edges: List[Tuple[str, str]]) -> List[str]:

    def is_gateway(node: str) -> bool:
        return node.isupper()

    graph: dict[str, set[str]] = defaultdict(set)
    gates: set[str] = set()

    for a, b in edges:
        graph[a].add(b)
        graph[b].add(a)
        if is_gateway(a):
            gates.add(a)
        if is_gateway(b):
            gates.add(b)

    for n in list(graph.keys()):
        graph[n]

    virus = "a"

    def bfs(start: str, allow=None) -> dict[str, int]:
        dist = {start: 0}
        q = deque([start])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if allow is not None and not allow(v):
                    continue
                if v not in dist:
                    dist[v] = dist[u] + 1
                    q.append(v)
        return dist

    def frontier_and_component(cur: str) -> tuple[list[tuple[str, str]], set[str]]:
        comp = set(bfs(cur, allow=str.islower).keys()) if cur in graph else set()
        front = set()
        for u in comp:
            for nbr in graph[u]:
                if is_gateway(nbr):
                    front.add((nbr, u))  # (G, u)
        return sorted(front), comp

    result: List[str] = []

    while True:
        front, comp = frontier_and_component(virus)
        if not front:
            break
        candidates = [e for e in front if e[1] == virus] or front
        G, u = min(candidates)

        if G in graph[u]:
            graph[u].remove(G)
        if u in graph[G]:
            graph[G].remove(u)
        result.append(f"{G}-{u}")

        front_after, _ = frontier_and_component(virus)
        if not front_after:
            break
        dist_from_v = bfs(virus)
        reachable_gates = [g for g in gates if g in dist_from_v]
        if not reachable_gates:
            break

        dmin = min(dist_from_v[g] for g in reachable_gates)
        candidates_gates = [g for g in reachable_gates if dist_from_v[g] == dmin]
        target_gate = min(candidates_gates)
        dist_to_gate = bfs(target_gate)
        next_steps = [
            n for n in graph[virus]
            if n.islower() and dist_to_gate.get(n, float("inf")) == dist_to_gate.get(virus, float("inf")) - 1
        ]
        if next_steps:
            virus = min(next_steps)
        else:
            break

    return result


def main():
    edges: List[Tuple[str, str]] = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        node1, sep, node2 = line.partition('-')
        if sep:
            edges.append((node1, node2))

    for cut in solve(edges):
        print(cut)


if __name__ == "__main__":
    main()
