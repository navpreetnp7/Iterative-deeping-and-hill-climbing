#!/usr/bin/env python
# coding: utf-8

# Submitted By :
#   Navpreet Singh
#   ns4767@nyu.edu



class Graph:
    
    #Undirected Graph with Vertices(with their associated cost) and Edges
    
    def __init__(self):
        self.Vertex = {}  # Vertex and its cost stored in a dictionary
        self.Edges = []   # List of all the edges [V1,V2]
        
    def addVertex(self,V,cost):  #method to add a new vertex
        self.Vertex[V] = cost
    
    def addEdge(self,V1,V2):    #method to add a new edge
        self.Edges.append([V1,V2])
        
        
    def nghbr(self,S):                          # method to return all the neighbours of state S
        nset = []                               # by adding or deleting one vertex in the set 
        n = len(S)
        for i in range(n):
            nset.append(S[0:i]+S[i+1:n])
        for v in self.Vertex:
            if v not in S:
                nset.append(S+[v])
        return nset
    
    
    
    
    def Vcost(self,S):                          # combined cost of all the vertices in a state   
        cst = 0
        for c in S:
            cst+=self.Vertex[c]
        return cst
    
    
    def f(self,S,T):                           # method to calculate the error function defined as
        cost1 = 0                              # Max(0,(Total cost of the vertices in S)-T) + the
        cost2 = 0                              # sum of the costs of all the uncovered edges E, where
                                               # the cost of an edge is considered to be the cost of its cheaper end.

        cost1 = self.Vcost(S)

        visited = {}
        for e in self.Edges:
            visited[tuple(e)]=False
        for v in S:
            for edge in visited:
                if v in edge:
                    visited[edge]=True
        for edge in visited:
            if not visited[edge]:
                cost2+=min(self.Vertex[edge[0]],self.Vertex[edge[1]])

        return max(0,cost1-T)+cost2
    
    
    
    
    def isGoalState(self,S):                    # To check whether the state is a goal state which is the state
        visited = {}                            # that covers all the edges
        for e in self.Edges:
            visited[tuple(e)]=False
        for v in S:
            for edge in visited:
                if v in edge:
                    visited[edge]=True
        for edge in visited:
            if not visited[edge]:
                return False
        return True


    def isEdgeCovered(self,S):                 # To check whether the successor state to the current state covers some 
        visited = {}                           # edge that is uncovered in the current state (otherwise it's pointless)
        for e in self.Edges:
            visited[tuple(e)]=False

        for v in S:
            covered = False
            for edge in visited:
                if not visited[edge] and v in edge :
                    visited[edge]=True
                    covered = True
            if not covered:
                return True
        return False
    
    
    def DFS(self,T,d,flag):                     # Depth First Search implementation till depth level 'd' and budget 'T'
        V = list(self.Vertex.keys())            # This function calls DFS1 which iterates recursively to the last
        found = False                           # depth of each state
        for v in self.Vertex:
            V.remove(v)
            if self.DFS1(T,v,V,d,flag):
                found = True
                break
        return found
    
    
    
    def DFS1(self,T,S,V,d,flag):                                    # DFS helper function to iterate recursively to the
        if len(S)>d or self.Vcost(S)>T or self.isEdgeCovered(S):    # depths of each state
            return False     #If cost exceeds budget or if the edges are already covered, then discard this successor state
        if flag == "V":
            print("{ ",end="")
            print(*S,end="")
            print(" }} Cost={}".format(self.Vcost(S)))
        if self.isGoalState(S):                         # Solution Found
            print("\nFound solution { ",end="")
            print(*S,end="")
            print(" }} Cost={}".format(self.Vcost(S)))
            return True
        V1 = V.copy()
        found = False
        for v in V:
            V1.remove(v)
            if self.DFS1(T,S+v,V1,d,flag):         #Recursively iterate to the maximum depth of the state
                found = True
                break
        return found
    
    
    
    def IterativeDeepening(self,T,flag):                          # Iterative Deepening Implementation with budget 'T'
        n = len(self.Vertex)                                      # It calls DFS upto depth 'd' which ranges 1 to n-1
        for i in range(n-1): #max depth = n-1
            if flag == "V":
                print("\nDepth = {}\n".format(i+1))
            if self.DFS(T,i+1,flag):
                break
    
    
    def HillClimbing(self,T,flag,S):                              # Hill Climbing Implementation with budget 'T' and 
        if flag == 'V':                                           # initial state 'S'
            print("{ ",end="")
            print(*sorted(S),end="")
            print(" }} Cost={} Error={}".format(self.Vcost(S),self.f(S,T)))

        while True:
            if flag == 'V':
                print("Neighbors:")
            N = self.nghbr(S)
            min = 10**6
            n1 = []

            for n in N:
                if flag == 'V':
                    print("{ ",end="")
                    print(*sorted(n),end="")
                    print(" }} Cost={} Error={}".format(self.Vcost(n),self.f(n,T)))
                if self.f(n,T) < min:
                    min = self.f(n,T)
                    n1 = n
                if self.f(n,T) == 0:
                    break

            if flag == 'V':
                print("\n")        
            if self.f(n1,T) >= self.f(S,T):
                return S
            if self.f(n1,T) == 0: #Error = 0. Goal state found.
                return n1
            S = n1       # Move to lowest error neighbour
            if flag == 'V':
                print("Move to { ",end="")
                print(*sorted(S),end="")
                print(" }} Cost={} Error={}".format(self.Vcost(S),self.f(S,T)))

    
    
    
    def randomRestartHillClimbing(self,T,flag,r):                       # Random Restart Hill Climbing that generates
        foundSol = False                                                # random starting state 'r' times and try to
                                                                        # find a solution using Hill Climbing
        for i in range(r):
            S = []

            #Choose a random state
            for v in self.Vertex:
                if random.randint(0,1):         # 50% probability for each vertex to be included in the random set
                    S.append(v)
            if len(S) == len(self.Vertex):      # Fix the invalid set when all the vertices are included in the random set by randomly removing some of them
                x = random.randint(1,len(S))
                for _ in range(x):
                    S.pop(random.randint(0,len(S)-1))

            if flag == 'V':
                print("-------Iteration {}----------\n\n".format(i+1))
                print("Randomly chosen start state: ",end="")
                print("{ ",end="")
                print(*S,end="")
                print(" }\n")

            G = self.HillClimbing(T,flag,S) #HillClimbing using the random state as starting state
            Error = self.f(G,T)
            if Error == 0:    # Solution Found
                print("Found Solution { ",end="")
                print(*sorted(G),end="")
                print(" }}. Cost={} Error={}".format(self.Vcost(G),Error))
                foundSol = True
                break
            else:     # No solution found in this iteration
                if flag == 'V':
                    print("Search Failed.\n")
        if not foundSol:    # No solution found after 'r' restarts
            print("\nNo solution found.")
    




import random

if __name__ == "__main__":
    
    
    with open('input.txt', 'r') as file:               # Read input from text file "input.txt"
        inputs = file.readlines()
    lines = [x.strip() for x in inputs]
    
    prob = ""
    
    if len(lines[0].split())==3:                       # if 3 inputs given in 1st line = T,flag,r then its a 
        T,flag,r = lines[0].split()                    # Random Restart Hill Climbing Problem
        prob = "RRHC"       #randomRestartHillClimbing
        r = int(r)
    elif len(lines[0].split())==2:                     # if 2 inputs given in 1st line = T,flag then its an 
        T,flag = lines[0].split()                      # Iterative Deepening Problem
        prob = "ID"         #IterativeDeepening
    T = int(T)
    
    g = Graph()                                       # Create a graph object and initialise it
    
    i = 1
                                                      # Start Taking Vertices and Edges from the input
    while lines[i] != "":
        vertex,cost = lines[i].split()
        g.addVertex(vertex,int(cost))                 # Add vertex and its cost to graph g
        i+=1
    i+=1
    while i<len(lines):
        v1,v2 = lines[i].split()
        g.addEdge(v1,v2)                              # Add edge to graph g
        i+=1
    
    """print(g.Vertex)
    print(g.Edges)"""
    
    # Run the programs depending on the input  
    
    if prob == "RRHC":
        g.randomRestartHillClimbing(T,flag,r)
    elif prob == "ID":
        g.IterativeDeepening(T,flag)
   





