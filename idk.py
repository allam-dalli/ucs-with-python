import heapq
import time
class Node:

	def __init__(self, key):

		self.key, self.successors, self.weight_successors = key, [], {}

	def getKey(self):
		return self.key

	def getSuccessors(self):
		return self.successors

	def addSuccessor(self, node, weight):
		if node.getKey() not in self.weight_successors:
			self.successors.append(node)
			self.weight_successors[node.getKey()] = weight

	def getWeightSuccessors(self):
		return self.weight_successors


class Graph:

	def __init__(self):
		self.nodes = {} 

	def addNode(self, key_node):
		if key_node in self.nodes: 
			print('Error: key %s already exists!!' % key_node)
		else:
			node = Node(key_node) 
			self.nodes[key_node] = node 

	def connect(self, key_source, key_destination, weight):
		if key_source in self.nodes and key_destination in self.nodes:
			if key_source != key_destination: 
				if weight > 0: 
					self.nodes[key_source].addSuccessor(self.nodes[key_destination], weight)
				else:
					print('Error: weight negative!!')
			else:
				print('Error: same keys!!')
		else:
			print('Error: key not exists!!')


	
	def getWeightEdge(self, key_source, key_successor):
		if key_source in self.nodes and key_successor in self.nodes: # checks if the keys exists
			if key_source != key_successor: # checks if the keys are differents
				weight_successors = self.nodes[key_source].getWeightSuccessors()
				if key_successor in weight_successors: # checks if key_successor is a successor
					return weight_successors[key_successor] # returns the weight
				else:
					print('Error: successor not exists!!')
			else:
				print('Error: same keys!!')
		else:
			print('Error: key not exists!!')


	def getSuccessors(self, key_node):
		if key_node in self.nodes:
			nodes = self.nodes[key_node].getSuccessors()
			keys_successors = [node.getKey() for node in nodes]
			return keys_successors
		else:
			print('Error: key not exists!!')


	def getNodes(self):
		return self.nodes




class PriorityQueue:

	def __init__(self):
		self._queue = []
		self._index = 0

	def insert(self, item, priority):
		heapq.heappush(self._queue, (priority, self._index, item))
		self._index += 1

	def remove(self):
		return heapq.heappop(self._queue)[-1]

	def is_empty(self):
		return len(self._queue) == 0





def run(graph, key_node_start, key_node_goal, verbose=False, time_sleep=0):
	if key_node_start not in graph.getNodes() or key_node_goal not in graph.getNodes():
		print('Error: key_node_start \'%s\' or key_node_goal \'%s\' not exists!!' % (key_node_start, key_node_goal))
	else:
		queue = PriorityQueue()

		keys_successors = graph.getSuccessors(key_node_start)

		for key_sucessor in keys_successors:
			weight = graph.getWeightEdge(key_node_start, key_sucessor)
			queue.insert((key_sucessor, weight), weight)


		reached_goal, cumulative_cost_goal = False, -1
		while not queue.is_empty():
			key_current_node, cost_node = queue.remove() 
			if(key_current_node == key_node_goal):
				reached_goal, cumulative_cost_goal = True, cost_node
				break

			if verbose:
				print('Expands node \'%s\' with cumulative cost %s ...' % (key_current_node, cost_node))
				time.sleep(time_sleep)

			keys_successors = graph.getSuccessors(key_current_node)

			if keys_successors: 
				for key_sucessor in keys_successors:
					cumulative_cost = graph.getWeightEdge(key_current_node, key_sucessor) + cost_node
					queue.insert((key_sucessor, cumulative_cost), cumulative_cost)

		if(reached_goal):
			print('\nReached goal! Cost: %s\n' % cumulative_cost_goal)
		else:
			print('\nUnfulfilled goal.\n')


if __name__ == "__main__":


	graph = Graph()
	graph.addNode('S') # start
	graph.addNode('a')
	graph.addNode('b')
	graph.addNode('c')
	graph.addNode('d')
	graph.addNode('e')
	graph.addNode('f') #goal
	graph.connect('S', 'a', 1)
	graph.connect('S', 'b', 10)
	graph.connect('S', 'c', 7)
	graph.connect('a', 'd', 2)
	graph.connect('a', 'e', 3)
	graph.connect('b', 'f', 3)
	graph.connect('c', 'f', 9)

	run(graph=graph, key_node_start='S', key_node_goal='f', verbose=True, time_sleep=2)