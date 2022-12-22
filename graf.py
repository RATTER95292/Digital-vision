import math
from sympy import Segment2D, Polygon
import networkx as nx


def tri(triangle, segment):
    inter = triangle.intersection(segment)
    if len(inter) == 0:
        return False
    if len(inter) == 2:
        return True
    if isinstance(inter[0], Segment2D):
        return False

    if len(inter) == 1:
        if triangle.encloses(segment.p1) or triangle.encloses(segment.p2):
            return True
        else:
            return False


def distance(edge):
    return math.sqrt((edge[0][0] - edge[1][0]) ** 2 + (edge[0][1] - edge[1][1]) ** 2)


def solve(dataset):
    start = tuple(map(int, dataset[0].split()))
    finish = tuple(map(int, dataset[1].split()))

    dataset = dataset[2:]

    shapes = []
    for line in dataset:
        line = list(map(int, line.split()))
        line = [(line[0], line[1]), (line[2], line[3]), (line[4], line[5])]
        shapes.append(line)

    obstacles = []
    for shape in shapes:
        obstacles.append(Polygon(*shape))

    points = []
    for shape in shapes:
        for point in shape:
            points.append(point)

    points.append(start)
    points.append(finish)

    vis_edges = []
    for i in range(len(points)):
        for j in points[i + 1 :]:
            seg = Segment2D(points[i], j)
            no_intersection = True
            for obs in obstacles:
                if tri(obs, seg):
                    no_intersection = False
                    break
            if no_intersection:
                vis_edges.append((points[i], j))

    G1 = nx.Graph()
    G1.add_edges_from(vis_edges)

    for edge in G1.edges:
        G1.add_edge(*edge, weight=distance(edge))

    shortest_path = nx.dijkstra_path(G1, start, finish, weight="weight")

    result = ""
    for i in range(len(shortest_path)):
        print(shortest_path[i][0], shortest_path[i][1])


n = int(input())
inp = []
for i in range(n):
    inp.append(input())

solve(inp)
