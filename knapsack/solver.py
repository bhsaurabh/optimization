#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # Turn this flag to True if debugging is being done
    debug = False

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])  # N
    capacity = int(firstLine[1])    # K

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    '''# a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight'''

    # Dynamic programming approach
    # Space is what we have to be careful about
    # (capacity + 1) rows and (item_count + 1) columns
    costs = []
    # For 0 items to be selected append a row of zeros
    costs.append([0] * (capacity+1))
    # now for remaining capacities
    for i in range(item_count):
        item = items[i]
        itemValue = item.value
        itemWeight = item.weight
        # holds all costs
        newList = []
        # loop over all capacities (0 ... K)
        for cap in range(capacity+1):
            # get previous cost
            prevCost = costs[i][cap]
            newCost = 0 # this has to change
            if itemWeight <= cap:
                newCost += (itemValue + costs[i][cap-itemWeight])
            if prevCost >= newCost:
                newCost = prevCost
            # update table
            newList.append(newCost)
        costs.append(newList)

    # print the cost table
    if debug:
        for cost in costs:
            print(cost)

    # now prepare data to be submitted
    value = costs[-1][-1]
    if debug:
        print('Optimum cost is: ' + str(value))

    taken = [0] * (item_count)
    j = -1
    for i in range(item_count-1, -1, -1):
        # get the costs array corresponding to this
        if (costs[i+1][j] != costs[i][j]):
            # this element was selected
            taken[i] = 1
            j -= items[i].weight

    if debug:
        print(taken)

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

