"""
Mini-Courier Planner
Algorithms: Merge Sort, 0/1 Knapsack (Dynamic Programming),
Dijkstra's Shortest Path, and Nearest Neighbor TSP approximation.
"""


import argparse
import csv
import heapq
import json
import random
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def merge_sort_parcels(parcels):
    """Sort parcels by earliest deadline, then highest priority."""
    if len(parcels) <= 1:
        return parcels[:]
    mid = len(parcels) // 2
    left = merge_sort_parcels(parcels[:mid])
    right = merge_sort_parcels(parcels[mid:])
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        a = (left[i]["deadline"], -left[i]["priority"])
        b = (right[j]["deadline"], -right[j]["priority"])
        if a <= b:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def knapsack_select(parcels, capacity):
    """Return maximum-value parcel subset fitting the weight capacity."""
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        weight = int(parcels[i - 1]["weight"])
        value = int(parcels[i - 1]["value"])
        for cap in range(capacity + 1):
            dp[i][cap] = dp[i - 1][cap]
            if weight <= cap:
                dp[i][cap] = max(
                    dp[i][cap],
                    value + dp[i - 1][cap - weight]
                )
    selected = []
    cap = capacity
    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i - 1][cap]:
            parcel = parcels[i - 1]
            selected.append(parcel)
            cap -= int(parcel["weight"])
    selected.reverse()
    return selected, dp[n][capacity], dp


def dijkstra(graph, source):
    """Find shortest distances and previous-node links from source."""
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[source] = 0
    heap = [(0, source)]
    while heap:
        current_distance, node = heapq.heappop(heap)
        if current_distance != distances[node]:
            continue
        for neighbor, weight in graph[node].items():
            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = node
                heapq.heappush(heap, (new_distance, neighbor))
    return distances, previous


def reconstruct_path(previous, destination):
    path = []
    node = destination
    while node is not None:
        path.append(node)
        node = previous[node]
    return list(reversed(path))


def nearest_neighbor_tsp(graph, start):
    """Build an approximate tour by repeatedly visiting nearest unvisited node."""
    unvisited = set(graph)
    unvisited.remove(start)
    route = [start]
    total = 0
    current = start
    while unvisited:
        choices = [
            (weight, neighbor)
            for neighbor, weight in graph[current].items()
            if neighbor in unvisited
        ]
        if not choices:
            raise ValueError("Graph is not connected to every remaining stop.")
        weight, next_node = min(choices)
        total += weight
        route.append(next_node)
        unvisited.remove(next_node)
        current = next_node
    if start in graph[current]:
        total += graph[current][start]
        route.append(start)
    return route, total


def load_data():
    with open(ROOT / "data" / "parcels.csv", newline="", encoding="utf-8") as f:
        parcels = [
            {**row, "weight": int(row["weight"]), "value": int(row["value"]),
             "priority": int(row["priority"]), "deadline": int(row["deadline"])}
            for row in csv.DictReader(f)
        ]
    with open(ROOT / "data" / "graph.json", encoding="utf-8") as f:
        graph = json.load(f)
    return parcels, graph


def run_project():
    parcels, graph = load_data()
    capacity = 15
    print("\n========== MINI-COURIER PLANNER ==========")
    print("\n1) Parcel prioritization (Merge Sort)")
    ordered = merge_sort_parcels(parcels)
    for p in ordered:
        print(f'{p["id"]}: {p["name"]}, deadline={p["deadline"]}, priority={p["priority"]}')

    print(f"\n2) Packing plan (0/1 Knapsack), capacity={capacity} kg")
    selected, value, _ = knapsack_select(ordered, capacity)
    total_weight = sum(p["weight"] for p in selected)
    print("Selected parcels:", ", ".join(p["id"] for p in selected))
    print(f"Total weight={total_weight} kg; total value={value}")

    print("\n3) Shortest paths (Dijkstra) from Depot")
    distances, previous = dijkstra(graph, "Depot")
    for destination in graph:
        print(f'{destination}: distance={distances[destination]}, '
              f'path={" -> ".join(reconstruct_path(previous, destination))}')

    print("\n4) Approximate delivery tour (Nearest Neighbor TSP)")
    route, length = nearest_neighbor_tsp(graph, "Depot")
    print("Route:", " -> ".join(route))
    print("Total tour distance:", length, "km")
    print("\nProject completed successfully.")


def benchmark():
    """Measure sorting and knapsack times on generated parcel sets."""
    random.seed(7)
    sizes = [20, 50, 100, 200, 400]
    rows = []
    for n in sizes:
        parcels = [
            {"id": str(i), "name": f"P{i}", "weight": random.randint(1, 10),
             "value": random.randint(10, 100), "priority": random.randint(1, 5),
             "deadline": random.randint(1, 30)}
            for i in range(n)
        ]
        t0 = time.perf_counter()
        merge_sort_parcels(parcels)
        sort_time = time.perf_counter() - t0
        # Keep capacity fixed so the DP measurement is comparable.
        t0 = time.perf_counter()
        knapsack_select(parcels, 100)
        knapsack_time = time.perf_counter() - t0
        rows.append({"input_size": n, "merge_sort_seconds": sort_time,
                     "knapsack_seconds": knapsack_time})
    out = ROOT / "results" / "benchmark.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print("Benchmark results saved to results/benchmark.csv")
    for row in rows:
        print(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mini-Courier Planner")
    parser.add_argument("--benchmark", action="store_true",
                        help="run algorithm performance tests")
    args = parser.parse_args()
    benchmark() if args.benchmark else run_project()