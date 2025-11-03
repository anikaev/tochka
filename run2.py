import sys
from collections import deque, defaultdict

def is_gateway(node: str) -> bool:
    return node.isupper()

def bfs_from(start, graph):
    INF = 10**9
    dist = {u: INF for u in graph}
    if start not in graph:
        return dist
    dist[start] = 0
    q = deque([start])
    while q:
        u = q.popleft()
        for v in graph[u]:
            if dist[v] == 10**9:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

def pick_target_gateway(virus, graph, gateways):
    dist = bfs_from(virus, graph)
    best = None
    best_d = 10**9
    for g in gateways:
        if dist.get(g, 10**9) < best_d:
            best_d = dist[g]
            best = g
        elif dist.get(g, 10**9) == best_d and best is not None and g < best:
            best = g
    return best, dist

def virus_next_step(virus, graph, target):
    if target is None:
        return virus  # путей нет — вирус не двигается
    INF = 10**9
    dist_from_target = {u: INF for u in graph}
    q = deque([target])
    dist_from_target[target] = 0
    while q:
        u = q.popleft()
        for v in graph[u]:
            if dist_from_target[v] == INF:
                dist_from_target[v] = dist_from_target[u] + 1
                q.append(v)

    dv = dist_from_target.get(virus, INF)
    if dv == INF:
        return virus
    candidates = [n for n in graph[virus] if dist_from_target.get(n, INF) == dv - 1]
    if not candidates:
        return virus
    return min(candidates)

def main():
    lines = [line.strip() for line in sys.stdin if line.strip()]
    graph = defaultdict(set)

    for line in lines:
        if '-' not in line:
            continue
        u, v = line.split('-', 1)
        graph[u].add(v)
        graph[v].add(u)

    if 'a' not in graph:
        graph['a'] = set()

    gateways = {u for u in graph if is_gateway(u)}
    virus = 'a'

    cuts = []

    def reachable_gateway():
        g, dist = pick_target_gateway(virus, graph, gateways)
        return g is not None and dist.get(g, 10**9) < 10**9

    steps_guard = 0
    while reachable_gateway():
        steps_guard += 1
        if steps_guard > 1000:
            break
        adjacent_gate_edges = sorted(
            [f"{g}-{virus}" if is_gateway(g) else f"{virus}-{g}"
             for g in graph[virus] if is_gateway(g)]
        )
        if adjacent_gate_edges:
            cut = adjacent_gate_edges[0]
            G, x = cut.split('-')
        else:
            target, dist_from_virus = pick_target_gateway(virus, graph, gateways)
            if target is None or dist_from_virus.get(target, 10**9) == 10**9:
                break
            dT = dist_from_virus[target]
            candidates = []
            for x in graph[target]:
                if dist_from_virus.get(x, 10**9) == dT - 1:
                    candidates.append(f"{target}-{x}")
            if not candidates:
                all_gw_edges = []
                for G in gateways:
                    for x in graph[G]:
                        if not is_gateway(x):
                            all_gw_edges.append(f"{G}-{x}")
                cut = min(all_gw_edges)
                G, x = cut.split('-')
            else:
                cut = min(candidates)
                G, x = cut.split('-')

        if x in graph[G]:
            graph[G].remove(x)
        if G in graph[x]:
            graph[x].remove(G)
        cuts.append(f"{G}-{x}")
        target_after, _ = pick_target_gateway(virus, graph, gateways)
        if target_after is None:
            break
        new_virus = virus_next_step(virus, graph, target_after)
        virus = new_virus

    for c in cuts:
        print(c)

if __name__ == "__main__":
    main()
