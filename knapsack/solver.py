#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def explore_tree(node, itemNumber, estimation, direction, errors, items, capacity, maxEst=None, maxNodes = []):
    '''
        Recursive method to explore tree nodes
        node = list that stores path taken
        itemNumber = item to be decided upon
        estimation = relaxed value
        direction = direction to take
        errors = errors to be allowed for
        items: the list of all items
        capacity = current capacity of knapsack
        maxEst: max estimation known
        maxNodes = Known configuration to output max value
    '''
    newNode = node[:]
    newEstimation = estimation
    newCapacity = capacity
    # Step 1: Explore based on direction. (If left, reject item)
    if direction == 'l':
        # reject the itemNumber
        newNode[itemNumber] = 0
        newEstimation -= items[itemNumber].value
    elif direction == 'r':
        # check if this is under our capacity
        if items[itemNumber].weight <= capacity:
            newNode[itemNumber] = 1
            newCapacity -= items[itemNumber].weight

    # Step 2: If this new node is a leaf node, return the value
    if itemNumber == len(items)-1:
        return newEstimation, newNode

    # Step 3: If previous max estimation is less than the current estimation...dont explore
    if maxEst is not None:
        if maxEst > newEstimation:
            return 0, []

    # Step 3: Recurse and move left, keeping track of estimation(s)
    maxEst2, maxNodes2 = explore_tree(newNode, itemNumber+1, newEstimation, 'l', errors, items, newCapacity, maxEst)

    if maxEst is None or maxEst2 > maxEst:
        maxEst = maxEst2
        maxNodes = maxNodes2

    # Step 4: Compare this estimation with right sub-tree and carry on
    maxEst3, maxNodes3 = 0, []
    if errors > 0:
        maxEst3, maxNodes3 = explore_tree(newNode, itemNumber+1, newEstimation, 'r', errors-1, items, newCapacity, maxEst)

    if maxEst is None or maxEst3 > maxEst:
        maxEst = maxEst3
        maxNodes = maxNodes3

    return maxEst, maxNodes



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

    # Branch and Bound method (Limited search)
    # Relaxation: Assume selection of all items
    relaxedCost = 0
    for item in items:
        # Assume that this item is selected
        relaxedCost += item.value

    if debug:
        print('Relaxed value upon selecting all items: ' + str(relaxedCost))

    # Now explore tree... hopefully we are looking at a pruned tree
    # the height of the tree is the number of items = item_capacity

    # provide some initial values
    maxValue = 0    # to be updated only on leaf node(s)
    maxTaken = []   # to be updated only on leaf node(s)

    # heuristic: going left is always correct, we break heurisitc numberOfFaults times
    numberOfFaults = 0
    maxEstimation = None
    maxNodes = []
    while numberOfFaults < capacity:
        # make different permutations here
        maxEst2, maxNodes2 = explore_tree([0]*item_count, 0, relaxedCost, 'l', numberOfFaults, items, capacity, maxEstimation, maxNodes)
        # Update maxEstimaiion and maxNodes
        if maxEstimation is None or maxEst2 > maxEstimation:
            maxEstimation = maxEst2
            maxNodes = maxNodes2
        # traverse right also if possible
        if numberOfFaults > 0:
            maxEst2, maxNodes2 = explore_tree([0]*item_count, 0, relaxedCost, 'r', numberOfFaults-1, items, capacity, maxEstimation, maxNodes)
        # Update maxEstimation and maxNodes
        if maxEstimation is None or maxEst2 > maxEstimation:
            maxEstimation = maxEst2
            maxNodes = maxNodes2
        # Update loop variable
        numberOfFaults += 1

    value = maxEstimation
    taken = maxNodes

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

