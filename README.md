# Mini-Courier Planner

## Requirements
- Python 3.9 or later
- No external Python packages are required to run `main.py`.
- The runtime chart was generated with Matplotlib.


## Files
- `main.py` — complete implementation
- `data/parcels.csv` — sample parcel dataset
- `data/graph.json` — road network represented as a weighted adjacency list
- `results/benchmark.csv` — measured runtime results
- `results/runtime_chart.png` — runtime chart
- `report.docx` — project report


## How to run
1. Run the application: `python main.py`
2. Run performance testing: `python main.py --benchmark`


## How to regenerate results
--- (if we need to change the data and regenerate our results then we have to run the following commands):
1. To regenerate sample_output.txt :
`python main.py > results\sample_output.txt`
2. To regenerate text_results.txt :
`python -m unittest -v test_main > results\test_results.txt 2>&1`


## Algorithms and complexity
1. Merge Sort: sorts by ascending deadline and then descending priority. Time: O(n log n); auxiliary space: O(n).
2. 0/1 Knapsack DP: maximizes total parcel value without exceeding capacity. Time: O(nW); space: O(nW), where W is capacity.
3. Dijkstra: computes shortest paths from the depot using a min-heap. With an adjacency list and binary heap: O((V+E) log V).
4. Nearest Neighbor TSP: repeatedly selects the nearest unvisited location. A straightforward implementation is approximately O(V^2); it is a heuristic and does not guarantee the globally shortest tour.


## Interpretation
The knapsack stage selects the most valuable combination subject to the weight limit. The route stage uses the supplied road graph and visits all graph locations. This sample project demonstrates the required algorithms; in a real courier service, parcel-to-destination mapping, traffic, vehicle limits and multiple vehicles would need further modelling.