from tcod import path
from sim_kls import Agent, Map, Spot

def get_path(map: Map, start_pos: Spot, end_pos: Spot) -> list[Spot]: # Abhängigkeit von map auflösen

    EUCLIDEAN = [  # Approximate euclidean distance.
        [99, 70, 99],
        [70, 0, 70],
        [99, 70, 99],
    ]

    graph = path.CustomGraph(map.grid.shape)
    graph.add_edges(edge_map=EUCLIDEAN, cost=map.grid)
    graph.set_heuristic(cardinal=70, diagonal=99)
    pf = path.Pathfinder(graph)
    pf.add_root(start_pos.get_block())
    walk_list = pf.path_to(end_pos.get_block())

    # print(pf.distance)

    walk =[]
    for x, y in walk_list:
        path_spot = Spot(x,y,1,map)
        walk.append(path_spot)
    return walk