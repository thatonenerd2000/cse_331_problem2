from Traversals import bfs_path
import heapq
from collections import deque
from Simulator import Simulator
import sys

class Solution: #test for functionality

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

    def maxBandList(self, clientList):
        bandwidths = self.info["bandwidths"]
        bandwidthsTuple = []
        bandwidthsNode = []

        for client in clientList:
            bandwidthsTuple.append((client,bandwidths[client]))

        bandwidthsTuple = sorted(bandwidthsTuple,key=lambda x: x[1])

        for (node,bandwidths) in bandwidthsTuple:
            bandwidthsNode.append(node)

        return bandwidthsNode

    def Reverse(self,clients):
        clients.reverse()
        return clients


    def modified_bfs_path(self, graph, isp, list_clients):
        paths = {}

        graph_size = len(graph)
        priors = [-1]*graph_size
        search_queue = deque()
        search_queue.append(isp)
        while search_queue:
            node = search_queue.popleft()
            clients = graph[node]
            clients = self.maxBandList(clients)
            clients = self.Reverse(clients)
            for neighbor in clients:
                if (priors[neighbor] == -1 and neighbor != isp):
                    priors[neighbor] = node
                    search_queue.append(neighbor)

        for client in list_clients:
            path = []
            current_node = client
            while (current_node != -1):
                path.append(current_node)
                current_node = priors[current_node]
            path = path[::-1]
            paths[client] = path

        return paths

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
        BFS will not work
        Polssible solution, run a traversal based on highest bandwidths
        '''
        paths = self.modified_bfs_path(graph,root,clients)
        #387: [2962, 5332, 7757, 1544, 387]
        #bfs:Revenue: 12219702.0
        #modified:Revenue: 7807747.0
        
        # Note: You do not need to modify all of the above. For Problem 1, only the paths variable needs to be modified. If you do modify a variable you are not supposed to, you might notice different revenues outputted by the Driver locally since the autograder will ignore the variables not relevant for the problem.
        # WARNING: DO NOT MODIFY THE LINE BELOW, OR BAD THINGS WILL HAPPEN
        return (paths, bandwidths, priorities)