from CBS.CBS import CBS
from CBS.CBSH import CBSH
from CBS.CBS_CP import CBS_CP
from CBS_DS.CBS_DS import CBS_DS
from CBS_Tree import CBS_tree
from CBS_DS.astar import distance
from map import Map
from work_with_file import read_task_from_file
from time import time

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs various MAPF algorithms')
    parser.add_argument('--file_name', type=str, default=None,
                        help='The name of file')
    parser.add_argument('--solver', type=str, default="CBS",
                        help='The solver to use (one of: {CBS,CBSH,CBS_CP,CBS_DS}), default CBS')

    args = parser.parse_args()

    width, height, cells, starts, goals = read_task_from_file(args.file_name)

    alg = None
    if args.solver == "CBS":
        alg = CBS
    elif args.solver == "CBS_DS":
        alg = CBS_DS
    else:
        print("???")
        exit(0)
    
    grid_map = Map()
    grid_map.set_grid_cells(width, height, cells)
    t1 = time()
    solution = alg(grid_map, starts, goals, distance, CBS_tree)
    t2 = time()
    print("TIME ", t2 - t1)
    print("COST: ", solution.get_cost())
    for i in range(len(starts)):
        print(solution.get_solution_of_robot(i).get_path())