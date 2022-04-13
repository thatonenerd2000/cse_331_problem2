from Traversals import bfs_path
import heapq
from collections import deque
from Simulator import Simulator
import sys

class Solution:

    def __init__(self, problem, isp, graph, info):
        self.problem = problem
        self.isp = isp
        self.graph = graph
        self.info = info

    '''
    param: self, list of nodes
    return: type:tuple, gets the highest bandwidth tuple of (node,bandwidths)
    '''
    def maxBand(self, clientList):
        bandwidths = self.info["bandwidths"]
        bandwidthsTyuple = []
        maxTuple = (0,0)
        for client in clientList:
            bandwidthsTyuple.append((client,bandwidths[client]))

        for every in bandwidthsTyuple:
            if every[1] > maxTuple[1]:
                maxTuple = (every[0],every[1])

        return maxTuple

    '''
    param: self, start node, end node, graph
    return: type:list a list of nodes in order from start to end
    THIS IS NOT COMPLETE YET, NOT SURE IF THIS WILL WORK EITHER
    Current Status: Stuck in infinite loop.
    '''
    def findPath(self,start,end,graph):
        startNode = graph[start]
        endNode = graph[end]
        backTrackNode = -1
        path = []

        #keeps track of the current node
        currentNode = start

        #Loops until reaches the end node
        while(currentNode != endNode):
            print(currentNode)
            #get the neighbor of the current node
            neighbor = graph[currentNode]
            #sanitize neighbor
            if backTrackNode in neighbor:
                neighbor.remove(backTrackNode)
            print(neighbor)
            #get the maxBandwith connected neighbor of the current node and append to path
            path.append(self.maxBand(neighbor)[0])
            backTrackNode = currentNode
            #replace the current node to the next node in the path
            currentNode = self.maxBand(neighbor)[0]


    def output_paths(self):
        """
        This method must be filled in by you. You may add other methods and subclasses as you see fit,
        but they must remain within the Solution class.
        """
        paths, bandwidths, priorities = {}, {}, {}

        #BFS will not work

        #same variables on the argument, but with references to self
        root = self.isp
        clients = self.info['list_clients']
        graph = self.graph

        '''
        Polssible solution, run a traversal based on highest bandwidths
        '''

        print(self.findPath(root,clients[clients.index(10839)],graph))
        
        # Note: You do not need to modify all of the above. For Problem 1, only the paths variable needs to be modified. If you do modify a variable you are not supposed to, you might notice different revenues outputted by the Driver locally since the autograder will ignore the variables not relevant for the problem.
        # WARNING: DO NOT MODIFY THE LINE BELOW, OR BAD THINGS WILL HAPPEN
        return (paths, bandwidths, priorities)
