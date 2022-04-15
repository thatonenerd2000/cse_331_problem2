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

    def getRoutingDelays(self, graph, root, clients, paths, bandwidths, priorities, is_rural):
        simulator = Simulator()
        simulator.run(graph, root, clients, paths, bandwidths, priorities, is_rural)

        return simulator.get_delays(clients)

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
    param: self, list of nodes
    return: type:list, gets the list order sorted of the given clienlist based on bandwidths
    '''
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

    '''
    param: self, list of nodes 1, list of nodes2
    return: type:list, gets the list order sorted of the given clienlist based on bandwidths
    '''
    def bandwidthCompare(self,clientList1, clientList2):
        cl1Total = 0
        cl2Total = 0
        bandwidths = self.info["bandwidths"]
        for clients in clientList1:
            cl1Total += bandwidths[clients]

        for clients in clientList2:
            cl2Total += bandwidths[clients]
            
        if cl1Total > cl2Total:
            return [clientList1,clientList2]

        else:
            return [clientList2,clientList1]

    '''
    param: self, paths 1, paths 2, list of clients
    return: type:paths, gets the path for each client with highest bandwidth from both traversals
    '''
    def compareBand(self, bfsPath, modifiedPath, clientsList):
        paths = {}
        for client in clientsList:
            bfsPathComp = bfsPath[client]
            modifiedPathComp = modifiedPath[client]
            greaterBand = self.bandwidthCompare(bfsPathComp,modifiedPathComp)
            if self.info["alphas"][client] >= 10:
                if len(greaterBand[0]) > len(greaterBand[1]):
                    paths[client] = greaterBand[1]
                else:
                    paths[client] = greaterBand[0]
            else:
                paths[client] = greaterBand[0]
        
        return paths

    '''
    param: self, paths 1, paths 2, list of clients, routingDelay of bfs, routingDelay of modified
    return: type:paths, gets the path for each client with lowest delays from both traversals
    '''
    def comparePaths(self, bfsPath, modifiedPath, clientsList, bfsDelays, modifiedDelays):
        paths = {}
        for client in clientsList:
            bfsPathComp = bfsPath[client]
            modifiedPathComp = modifiedPath[client]
            bfsDelay = bfsDelays[client]
            modifiedDelay =  modifiedDelays[client]

            if bfsDelay > modifiedDelay:
                paths[client] = modifiedPathComp
            else:
                paths[client] = bfsPathComp

        return paths




    '''
    param: self, list of nodes
    return: type:list, reverses the given list
    '''
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
        bandwidths = self.info['bandwidths'] if not None else None
        is_rural = None if 'is_rural' not in self.info else self.info['is_rural']

        modifiedTraversal = self.modified_bfs_path(graph,root,clients)
        bfsTraversal = bfs_path(graph,root,clients)

        routingDelaysBFS = self.getRoutingDelays(self.graph, self.isp, self.info["list_clients"], bfsTraversal, bandwidths, 0, is_rural)
        routingDelayModified = self.getRoutingDelays(self.graph, self.isp, self.info["list_clients"], modifiedTraversal, bandwidths, 0, is_rural)

        # paths = self.compareBand(bfsTraversal,modifiedTraversal,clients,routingDelaysBFS,routingDelayModified)
        paths = self.comparePaths(bfsTraversal, modifiedTraversal, clients, routingDelaysBFS, routingDelayModified)

        # print(self.info["alphas"])
        #387: [2962, 5332, 7757, 1544, 387]
        #bfs:Revenue: 12219702.0
        #modified:Revenue: 7807747.0
        #compareModified:Revenue: 13199927.0
        #compareModfiedRoutingDelays: Revenue: 13487968.0


        # Note: You do not need to modify all of the above. For Problem 1, only the paths variable needs to be modified. If you do modify a variable you are not supposed to, you might notice different revenues outputted by the Driver locally since the autograder will ignore the variables not relevant for the problem.
        # WARNING: DO NOT MODIFY THE LINE BELOW, OR BAD THINGS WILL HAPPEN
        return (paths, bandwidths, priorities)
