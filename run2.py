import sys
from collections import deque, defaultdict
from typing import List, Tuple

def solve(edges: List[Tuple[str, str]]) -> List[str]:
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    def is_gate(x: str) -> bool:
        return len(x) == 1 and x.isupper()

    def is_node(x: str) -> bool:
        return len(x) == 1 and x.islower()

    def all_gates() -> List[str]:
        return sorted([n for n in adj if is_gate(n)])

    def bfs_from(src: str) -> dict:
        dist = {src: 0}
        q = deque([src])
        while q:
            u = q.popleft()
            for w in adj[u]:
                if w not in dist:
                    dist[w] = dist[u] + 1
                    q.append(w)
        return dist

    def nearest_gate_from(v: str):
        dist = bfs_from(v)
        candidates = [(dist[g], g) for g in all_gates() if g in dist]
        if not candidates:
            return None, None, dist
        L, g = min(candidates)
        return g, L, dist

    result: List[str] = []
    virus = 'a'

    while True:
        g, L, dist_from_v = nearest_gate_from(virus)
        if g is None:
            break

        if L == 1:
            gates_adj = sorted([w for w in adj[virus] if is_gate(w)])
            cut_gate, cut_node = gates_adj[0], virus
        else:
            candidates = [n for n in adj[g] if is_node(n) and n in dist_from_v and dist_from_v[n] + 1 == L]
            if not candidates:
                ok = False
                for g2 in all_gates():
                    if g2 in dist_from_v:
                        L2 = dist_from_v[g2]
                        cand2 = [n for n in adj[g2] if is_node(n) and n in dist_from_v and dist_from_v[n] + 1 == L2]
                        if cand2:
                            g, L, candidates, ok = g2, L2, cand2, True
                            break
                if not ok:
                    break
            cut_gate = g
            cut_node = sorted(candidates)[0]

        result.append(f"{cut_gate}-{cut_node}")
        if cut_node in adj[cut_gate]:
            adj[cut_gate].remove(cut_node)
        if cut_gate in adj[cut_node]:
            adj[cut_node].remove(cut_gate)
        g_after, L_after, _ = nearest_gate_from(virus)
        if g_after is None:
            break
        dist_to_target = bfs_from(g_after)
        if virus not in dist_to_target:
            break
        next_steps = [u for u in adj[virus]
                      if is_node(u) and u in dist_to_target and dist_to_target[u] == dist_to_target[virus] - 1]
        if not next_steps:
            break
        virus = sorted(next_steps)[0]

    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()
