from collections import deque
import heapq
import sys

def parsing(grid):
    h, w = len(grid), len(grid[0])
    start = []
    kmap = {}
    for row in range(h):
        for col in range(w):
            ch = grid[row][col]
            if ch == '@':
                start.append((row, col))
            elif 'a' <= ch <= 'z':
                kmap[ch] = (row, col)
    ksort = sorted(kmap)
    kidx = {ch: i for i, ch in enumerate(ksort)}
    return h, w, start, kmap, kidx

def sobir(grid, h, w, start, kmap, kidx):
    node = start + [kmap[ch] for ch in sorted(kidx, key=lambda x: kidx[x])]
    knode = [None] * len(start) + sorted(kidx, key=lambda x: kidx[x])
    adj = [[] for _ in node]
    dir = [(1,0),(-1,0),(0,1),(0,-1)]

    for u, (sr, sc) in enumerate(node):
        visited = [[False]*w for _ in range(h)]
        queue = deque([(sr, sc, 0, set())])
        visited[sr][sc] = True

        while queue:
            r, c, dist, door = queue.popleft()
            for dr, dc in dir:
                nr,nc = r+dr, c+dc
                if not (0 <= nr < h and 0 <= nc < w):
                    continue
                if visited[nr][nc] or grid[nr][nc] == '#':
                    continue

                visited[nr][nc] = True
                ch = grid[nr][nc]
                nw_door = door.copy()
                if 'A' <= ch <= 'Z':
                    nw_door.add(ch.lower())

                if 'a' <= ch <= 'z':
                    v = 4 + kidx[ch]
                    adj[u].append((v, dist + 1, nw_door))

                queue.append((nr, nc, dist + 1, nw_door))

    return adj, knode

def poisk(adj, node_to_key):
    klist = node_to_key[4:]
    CONST = frozenset(klist)
    st_state = (frozenset(), (0, 1, 2, 3))
    dist = {st_state: 0}
    heap = [(0, frozenset(), (0,1,2,3))]

    while heap:
        d, collected, rb = heapq.heappop(heap)
        if d > dist[(collected, rb)]:
            continue
        if collected == CONST:
            return d

        for i in range(4):
            u = rb[i]
            for v, w_uv, need in adj[u]:
                if not need.issubset(collected):
                    continue
                key = node_to_key[v]
                if key in collected:
                    continue

                nw_clt = collected | {key}
                new_rb = list(rb)
                new_rb[i] = v
                new_rb = tuple(new_rb)
                nd = d + w_uv
                state = (nw_clt, new_rb)

                if nd < dist.get(state, float('inf')):
                    dist[state] = nd
                    heapq.heappush(heap, (nd, nw_clt, new_rb))

    return -1

def min_steps_to_collect_all_keys(grid):
    h,w,start,kmap, kidx = parsing(grid)
    if not kidx:
        return 0
    adj, node_to_key = sobir(grid,h, w,start, kmap,kidx)
    return poisk(adj, node_to_key)

if __name__ == "__main__":
    grid = []
    while True:
        line = input()
        if line.strip() == "":
            break
        grid.append(line)

    result = min_steps_to_collect_all_keys(grid)
    print(result)
