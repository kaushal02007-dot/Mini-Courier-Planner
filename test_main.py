import unittest
from main import merge_sort_parcels, knapsack_select, dijkstra, nearest_neighbor_tsp

class CourierTests(unittest.TestCase):
    def test_sort_order(self):
        p=[{"deadline":2,"priority":1},{"deadline":1,"priority":1},{"deadline":1,"priority":5}]
        out=merge_sort_parcels(p)
        self.assertEqual([(x["deadline"],x["priority"]) for x in out],[(1,5),(1,1),(2,1)])

    def test_knapsack_capacity(self):
        p=[{"weight":2,"value":10},{"weight":3,"value":15},{"weight":4,"value":20}]
        chosen,value,_=knapsack_select(p,5)
        self.assertLessEqual(sum(x["weight"] for x in chosen),5)
        self.assertEqual(value,25)

    def test_dijkstra(self):
        g={"S":{"A":2,"B":8},"A":{"S":2,"B":1},"B":{"S":8,"A":1}}
        dist,_=dijkstra(g,"S")
        self.assertEqual(dist["B"],3)

    def test_tour(self):
        g={"S":{"A":1,"B":4},"A":{"S":1,"B":2},"B":{"S":4,"A":2}}
        route,total=nearest_neighbor_tsp(g,"S")
        self.assertEqual(route,["S","A","B","S"])
        self.assertEqual(total,7)

if __name__=="__main__":
    unittest.main()
