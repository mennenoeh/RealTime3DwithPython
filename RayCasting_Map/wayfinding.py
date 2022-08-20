from tcod import path
from sim_kls import Map

def get_path(map: Map, start_pos: tuple[int, int], end_pos: tuple[int, int]) -> list[tuple[int, int]]: # Abhängigkeit von map auflösen

    EUCLIDEAN = [  # Approximate euclidean distance.
        [99, 70, 99],
        [70, 0, 70],
        [99, 70, 99],
    ]

    graph = path.CustomGraph(map.cells.shape)
    graph.add_edges(edge_map=EUCLIDEAN, cost=map.get_blocked_cells())
    graph.set_heuristic(cardinal=70, diagonal=99)
    pf = path.Pathfinder(graph)
    pf.add_root(start_pos)
    return pf.path_to(end_pos).tolist()

    print(pf.distance)