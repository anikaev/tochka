import sys
from collections import deque

def isolate_virus(corridors):
    graph = {}
    gateways = set()
    for corridor in corridors:
        u, v = corridor.split('-')
        graph.setdefault(u, []).append(v)
        graph.setdefault(v, []).append(u)
        if u.isupper():
            gateways.add(u)
        if v.isupper():
            gateways.add(v)
    virus_node = 'a'
    result = []

    def bfs_distances(start):
        dist = {start: 0}
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor in graph.get(node, []):
                if neighbor not in dist:
                    dist[neighbor] = dist[node] + 1
                    queue.append(neighbor)
        return dist

    while True:
        neighbors = graph.get(virus_node, [])
        gateway_neighbors = [node for node in neighbors if node in gateways]
        if gateway_neighbors:
            gateway_neighbors.sort()
            g = gateway_neighbors[0]
            graph[g].remove(virus_node)
            graph[virus_node].remove(g)
            result.append(f"{g}-{virus_node}")
        else:
            dist = bfs_distances(virus_node)
            reachable_gateways = [(dist[g], g) for g in gateways if g in dist]
            if not reachable_gateways:
                break
            min_dist = min(d for d, g in reachable_gateways)
            candidates = [g for d, g in reachable_gateways if d == min_dist]
            candidates.sort()
            target_gateway = candidates[0]
            gateway_links = [node for node in graph[target_gateway]]
            gateway_links.sort()
            if not gateway_links:
                break
            node_to_cut = gateway_links[0]
            graph[target_gateway].remove(node_to_cut)
            graph[node_to_cut].remove(target_gateway)
            result.append(f"{target_gateway}-{node_to_cut}")

        dist_after = bfs_distances(virus_node)
        reachable_gateways = [(dist_after[g], g) for g in gateways if g in dist_after]
        if not reachable_gateways:
            break
        min_dist = min(d for d, g in reachable_gateways)
        candidates = [g for d, g in reachable_gateways if d == min_dist]
        candidates.sort()
        new_target = candidates[0]

        dist_from_target = bfs_distances(new_target)
        next_steps = []
        for nei in sorted(graph.get(virus_node, [])):
            if nei in dist_from_target and virus_node in dist_from_target:
                if dist_from_target[nei] == dist_from_target[virus_node] - 1:
                    next_steps.append(nei)
        if next_steps:
            virus_node = next_steps[0]
        else:
            break
    return result


def main():
    corridors = []
    for line in sys.stdin:
        s = line.strip()
        if not s:
            continue
        if '-' in s:
            u, sep, v = s.partition('-')
            if u and v:
                corridors.append(f"{u.strip()}-{v.strip()}")

    for cut in isolate_virus(corridors):
        print(cut)


if __name__ == "__main__":
    main()
