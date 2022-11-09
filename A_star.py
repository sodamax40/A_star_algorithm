import pandas as pd
import numpy as np
from collections import OrderedDict

# add some comment

data = pd.read_csv(
    r'/Users/youdengsong/Desktop/master_course/Artificial_intelligent/assign_1/100_nodes.csv')
df = pd.DataFrame(data, columns=['x', 'y'])


def heuristic_cost(state, goal):
    x_sub = abs(df.iat[state, 0] - df.iat[goal, 0])
    y_sub = abs(df.iat[state, 1] - df.iat[goal, 1])
    return 1 / 2 * (x_sub + y_sub)


def search_best_node(frontier, weight, goal):
    f_best = np.inf
    for key in frontier:
        n = frontier[key]
        h = heuristic_cost(n['state'], goal)
        if weight * n['cost'] + (1 - weight) * h < f_best:
            f_best = weight * n['cost'] + (1 - weight) * h
            i_best = key
    node = frontier[i_best]
    frontier.pop(i_best)
    return node


def expand_graph_search(node, reach):
    child_list = OrderedDict()
    state = node["state"]
    for i in range(3, 103):
        if data.iat[state, i] != 0:
            cost = node["cost"] + data.iat[state, i]
            child_name = "node" + str(i - 3)
            if child_name in reach.keys():
                continue
            else:
                child_list[child_name] = {
                    "state": i - 3, "parent": state, "action": data.iat[state, i], "cost": cost}
    return child_list


def search(reach, child_list):
    flag = -1
    for key in reach:
        if (reach[key]['state'] == child_list['state']):
            flag = 1
        else:
            flag = -1
    return flag


def algorithm(start, goal, weight):
    frontier = OrderedDict()
    reach = OrderedDict()

    node = {"state": start, "cost": 0, "path": []}
    node_name = "node" + str(start)
    frontier[node_name] = node
    reach[node_name] = node
    path_node = {}
    path = []

    while bool(frontier):
        n = search_best_node(frontier, weight, goal)
        node_name = 'node' + str(n['state'])
        path_node[node_name] = n
        if n['state'] == goal:
            node_name = 'node' + str(n['state'])
            path.append(n['state'])
            parent_num = n['parent']

            while (parent_num != start):

                path.append(parent_num)
                node_name = 'node' + str(parent_num)
                parent_num = path_node[node_name]['parent']
            path.append(start)
            path.reverse()
            print("path sequence:", path)
            print("lenth of the path:", len(path))
            print("Number of nodes generate:", len(reach))
            print("total distance:", n['cost'])
            return n

        child_list = expand_graph_search(n, reach)
        for key in child_list:
            index = search(reach, child_list[key])
            if index == -1:
                frontier[key] = child_list[key]
                reach[key] = child_list[key]
            elif child_list[key]["cost"] < reach[key]["cost"]:
                reach[key] = child_list[key]
                frontier[key] = child_list[key]
    return "no path found"


start = input('type in your start ')
goal = input('type in your Goal ')
weight = input('type in your weight ')
algorithm(int(start), int(goal), float(weight))
