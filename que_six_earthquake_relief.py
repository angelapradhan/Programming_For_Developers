import math
import heapq

def solve_safest_logistics():
    graph = {
        'KTM': {'JA': 0.90, 'JB': 0.80},
        'JA':  {'KTM': 0.90, 'PH': 0.95, 'BS': 0.70},
        'JB':  {'KTM': 0.80, 'JA': 0.60, 'BS': 0.90},
        'PH':  {'JA': 0.95, 'BS': 0.85},
        'BS':  {'JA': 0.70, 'JB': 0.90, 'PH': 0.85}
    }

    start_node = 'KTM'
    
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    predecessors = {node: None for node in graph}
    pq = [(0, start_node)]

    while pq:
        current_distance, u = heapq.heappop(pq)

        if current_distance > distances[u]:
            continue

        for v, probability in graph[u].items():
            weight = -math.log(probability)
            distance = current_distance + weight

            if distance < distances[v]:
                distances[v] = distance
                predecessors[v] = u
                heapq.heappush(pq, (distance, v))

    print(f"{'Destination':<15} | {'Safest Path':<20} | {'Safety Probability'}")
    print("-" * 55)

    for node in graph:
        if node == start_node: continue
        
        path = []
        curr = node
        while curr:
            path.append(curr)
            curr = predecessors[curr]
        path_str = " -> ".join(reversed(path))
        
        actual_safety = math.exp(-distances[node])
        
        print(f"{node:<15} | {path_str:<20} | {actual_safety:.4f}")

if __name__ == "__main__":
    solve_safest_logistics()