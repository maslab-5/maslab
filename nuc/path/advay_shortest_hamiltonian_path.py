from sys import maxsize 
from itertools import permutations
import math
import heapq

import numpy as np

def segments_distance(x11, y11, x12, y12, x21, y21, x22, y22):
	if segments_intersect(x11, y11, x12, y12, x21, y21, x22, y22):
		return 0
	# try each of the 4 vertices w/the other segment
	distances = []
	distances.append(point_segment_distance(x11, y11, x21, y21, x22, y22))
	distances.append(point_segment_distance(x12, y12, x21, y21, x22, y22))
	distances.append(point_segment_distance(x21, y21, x11, y11, x12, y12))
	distances.append(point_segment_distance(x22, y22, x11, y11, x12, y12))
	return min(distances)

def segments_intersect(x11, y11, x12, y12, x21, y21, x22, y22):
	""" whether two segments in the plane intersect:
	one segment is (x11, y11) to (x12, y12)
	the other is   (x21, y21) to (x22, y22)
	"""
	dx1 = x12 - x11
	dy1 = y12 - y11
	dx2 = x22 - x21
	dy2 = y22 - y21
	delta = dx2 * dy1 - dy2 * dx1
	if delta == 0: return False  # parallel segments
	s = (dx1 * (y21 - y11) + dy1 * (x11 - x21)) / delta
	t = (dx2 * (y11 - y21) + dy2 * (x21 - x11)) / (-delta)
	return (0 <= s <= 1) and (0 <= t <= 1)

import math
def point_segment_distance(px, py, x1, y1, x2, y2):
	dx = x2 - x1
	dy = y2 - y1
	if dx == dy == 0:  # the segment's just a point
		return math.hypot(px - x1, py - y1)

	# Calculate the t that minimizes the distance.
	t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)

	# See if this represents one of the segment's
	# end points or a point in the middle.
	if t < 0:
		dx = px - x1
		dy = py - y1
	elif t > 1:
		dx = px - x2
		dy = py - y2
	else:
		near_x = x1 + t * dx
		near_y = y1 + t * dy
		dx = px - near_x
		dy = py - near_y

	return math.hypot(dx, dy)

def make_graph(maxX, maxY, startX, startY, stacks, walls):
	robot_width = 0.6
	def wall_in_way(v1, v2):
		for wall in walls:
			dist = segments_distance(v1[0], v1[1], v2[0], v2[1], wall[0][0], wall[0][1], wall[1][0], wall[1][1])
			if dist < robot_width/2:
				return True
		for stack in stacks:
			if v2[0] == stack[0] and v2[1] == stack[1]:
				break
			dist = segments_distance(v1[0], v1[1], v2[0], v2[1], stack[0], stack[1], stack[0] + 0.0001, stack[1]+0.0001)
			if dist < 0.3:
				return True
		return False

	G = {}
	for i in range(2*maxX):
		for j in range(2*maxY):
			for k in range(2*maxX):
				for l in range(2*maxY):
					if i==k and j==l:
						continue
					else:
						if (i/2,j/2) not in G:
							G[(i/2,j/2)] = {}
						if (k/2,l/2) not in G:
							G[(k/2,l/2)] = {}

						if not wall_in_way((i/2,j/2), (k/2,l/2)):
							G[(i/2,j/2)][(k/2,l/2)] = ((i/2-k/2)**2 + (j/2-l/2)**2)**0.5
							G[(k/2,l/2)][(i/2,j/2)] = ((i/2-k/2)**2 + (j/2-l/2)**2)**0.5
			#in case any stack is not a lattice point 
			for stack in stacks:
				if (stack[0], stack[1]) not in G:
					G[(stack[0], stack[1])] = {}
				if not wall_in_way((i/2,j/2), (stack[0], stack[1])):
					G[(i/2,j/2)][(stack[0], stack[1])] = ((i/2 - stack[0])**2 + (j/2-stack[1])**2)**0.5
					G[(stack[0], stack[1])][(i/2,j/2)] = ((i/2 - stack[0])**2 + (j/2-stack[1])**2)**0.5

	#handle case of start position not being a lattice point
	if (startX, startY) not in G:
		G[(startX, startY)] = {}
		for stack in stacks:
			if not wall_in_way((startX, startY), (stack[0], stack[1])):
				G[(startX, startY)][(stack[0], stack[1])] = ((startX - stack[0])**2 + (startY-stack[1])**2)**0.5
				G[(stack[0], stack[1])][(startX,startY)] = ((startX - stack[0])**2 + (startY-stack[1])**2)**0.5
		for i in range(2*maxX):
			for j in range(2*maxY):
				if not wall_in_way((startX, startY), (i/2,j/2)):
					G[(i/2,j/2)][(startX, startY)] = ((i/2-startX)**2 + (j/2-startY)**2)**0.5
					G[(startX, startY)][(i/2,j/2)] = ((i/2-startX)**2 + (j/2-startY)**2)**0.5


	return G


def travellingSalesmanProblem(graph, s, stacks):

	def min_path(G, start, finish):

		def euclidean(vertex, finish):
			return ((vertex[0]-finish[0])**2 + (vertex[1] - finish[1])**2)**0.5

		if finish in G[start]:
			return G[start][finish], finish

		opened = []
		heapq.heappush(opened, (0, (start,)))
		while opened:
			curr_dist, curr = heapq.heappop(opened)
			print(curr)
			if curr[-1] == finish:
				return curr_dist, curr
			min_dist = float('inf')
			min_travel = None
			best = None
			for vertex in G[curr[-1]]:
				if vertex in curr:
					continue
				dist = G[curr[-1]][vertex] + euclidean(vertex, finish)
				heapq.heappush(opened, (curr_dist + dist, curr + (vertex,)))
				

		return None

	print("HELLO")
	print(min_path(G,(1.0, 2.0), (5.0, 3.0)))
	# store all vertex apart from source vertex 
	vertex = [] 
	for v in stacks:
		vertex.append((v[0], v[1]))
	# store minimum weight Hamiltonian Cycle 
	min_length  = float('inf')
	answer = None
	next_permutation=permutations(vertex)
	for i in next_permutation:
		curr_path = [(s[0],s[1])]
	# store current Path weight(cost) 
		current_pathweight = 0

			# compute current path weight 
		finished = True
		curr = s 
		for j in i: 
			result = min_path(G, curr, j)
			if result is None:
				finished = False
				break
			length, path = result[0], result[1]
			current_pathweight += length
			curr_path.append(path)
			curr = j  
		if not finished:
			continue
		if current_pathweight < min_length:
			min_length = current_pathweight
			answer = curr_path
		#print(i, current_pathweight)
	return (answer, min_length)

maxX = 10
maxY = 10
startX= 0.5
startY= 0.5
stacks= [[1.0, 2.0, [False, True, False]], [2.0, 1.0, [False, True, False]], [3.0, 3.0, [False, True, False]], [4.0, 4.0, [False, True, False]], [5.0, 3.0, [False, True, False]]]
walls= [[[2,2],[2,3]],[[0, 1.5], [1,1.5]],[[1.0, 5.0], [6.0, 5.0]], [[6.0, 5.0], [6.0, 2.0]], [[6.0, 2.0], [5.0, 2.0]], [[5.0, 2.0], [5.0, 1.0]], [[5.0, 1.0], [3.0, 1.0]], [[3.0, 1.0], [3.0, 0.0]], [[3.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 3.0]], [[0.0, 3.0], [1.0, 3.0]], [[1.0, 3.0], [1.0, 5.0]]]
G = make_graph(maxX, maxY, startX, startY, stacks, walls)
print(len(G.keys()))
#print(G[(2,1)])
#print(segments_distance(0,10,1,10,0,0,1,0))
print(travellingSalesmanProblem(G, (startX, startY), stacks))
