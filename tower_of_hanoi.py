import copy
from copy import deepcopy


"""
Objects of class game_state represent states of the tower of hanoi game. 

The objects hold the value of their parent state, representation of the game state as a list of lists, and have a class method to calculate the list of 
legal moves from the current state.
"""
class game_state:
	def __init__(self):
		self.parent = []
		self.pegs = [];
		self.next_moves = [];

	def __init__(self, state, parent):
		self.parent = parent
		self.pegs = state
		self.next_moves = []

	def get_all_valid_moves(self):
		for this_peg in range(len(self.pegs)):
			for other_pegs in range(len(self.pegs)):
				if this_peg!=other_pegs and self.pegs[this_peg]:
					if not self.pegs[other_pegs] or self.pegs[this_peg][-1]<self.pegs[other_pegs][-1]:
						new_state = copy.deepcopy(self.pegs)
						new_state[other_pegs].append(new_state[this_peg].pop())
						self.next_moves.append(new_state)




def remove_duplicates(past_move_list, current_state):
	"""
	This method removes any previously performed moves from the pool of valid moves performable from current_state.
	"""
	no_dupe_next_moves = []
	for move in current_state.next_moves:
		flag = True
		for completed_move in past_move_list:
			if move == completed_move:
				flag = False
				break
		if flag:
			no_dupe_next_moves.append(move)
	current_state.next_moves = no_dupe_next_moves




def get_traversal(end_state):
	"""
	This is a path display method. After reaching the goal state, the 'parent' value of the goal state object is used to trace the path taken
	from the start state.
	"""
	state = end_state
	traversal = []
	trace = []
	num = 0
	traversal.append(state.pegs)
	while state.parent:
		traversal.append(state.parent.pegs)
		state = state.parent
	while traversal:
		num+=1
		item = traversal.pop()
		trace.append(item)
		print str(item)+'\n'
	print 'Steps: '+str(num)
	



def bfs(root, end_state):
	"""
	This performs breadth-first-search to find the goal state.
	A queue is maintained which holds all possible moves that can be made from current state. Each item in the queue is checked against the goal state. 
	If an item matches the goal state, it is returned and search is completed. If there is no match, all possible moves from that state are added to the 
	queue (barring repeated moves).This process continues until the goal state is found or the queue is empty.
	"""
	all_move_list = []
	all_move_list += root.pegs
	root.get_all_valid_moves()
	possible_states = []
	for move in root.next_moves:
		possible_states.append(game_state(move, root))
	all_move_list += root.next_moves
	while possible_states:
		current_state = possible_states.pop(0)
		if current_state.pegs == end_state:
			get_traversal(current_state)
		else:
			current_state.get_all_valid_moves()
			remove_duplicates(all_move_list, current_state)
			all_move_list += current_state.next_moves
			for move in current_state.next_moves:
				possible_states.append(game_state(move,current_state))




def dfs(root, end_state):
	"""
	Helper function for depth-first-search.
	"""
	all_move_list = []
	all_move_list.append(root.pegs)
	goal_state = depth_first_search(root, end_state, all_move_list)
	get_traversal(goal_state)


def depth_first_search(root, end_state, all_move_list):
	"""
	This function performs depth-first-search to find the goal state.
	The function is called recursively, with the first valid move from current state being passed as root for each function call till goal state is
	reached or all possible states resulting from the original valid move have been explored. The process is then repeated for the next valid move and all states 
	stemming from there, and so on.
	"""
	if root.pegs == end_state:
		return root
	else:
		root.get_all_valid_moves()
		remove_duplicates(all_move_list, root)
		for move in root.next_moves:
			new_move = game_state(move, root)
			all_move_list.append(move)
			goal = depth_first_search(new_move, end_state, all_move_list)
			if goal:
				return goal




def rank_moves_user_defined(possible_states, end_state):
	"""
	Helper function to carry out shortest distance calculation between next valid moves and goal state. Priority queue is formed based on these calculations.
	Heuristic works as follows:
	- finds sum of values of disks on each peg of goal state 
	- for each state/move from list of possible moves, the values of disks on each peg are summed
	- absolute difference between the peg values for said state and the goal state is calculated
	- the absolute distance values of all pegs are summed to determine a 'distance' value for the move
	- This is repeated for each possible move
	- next_moves list is re-ordered in ascending order of 'distance'  
	"""
	reordered_list = []
	end_state_sum = []
	move_weights = []
	for item in end_state:
		end_state_sum.append(sum(item))
	for state in possible_states:
		move = state.pegs
		move_sum = []
		abs_value = []
		for item in move:
			move_sum.append(sum(item))
		difference = [a-b for a,b in zip(end_state_sum,move_sum)]
		for item in difference:
			abs_value.append(abs(item))
		move_weights.append(sum(abs_value))
	while possible_states:		
		closest = move_weights.index(min(move_weights))
		move_weights.pop(closest)
		reordered_list.append(possible_states.pop(closest))
	return reordered_list


def bestfs(root, end_state):
	"""
	Performs best-first-search in order to find a path to the goal state.
	Best first search functions similarly to breadth-first search, but uses a heuristic to prioritize the valid moves queue in terms of distance from goal state. 
	"""
	all_move_list = []
	all_move_list += root.pegs
	root.get_all_valid_moves()
	possible_states = []
	for move in root.next_moves:
		possible_states.append(game_state(move, root))
	possible_states = rank_moves_user_defined(possible_states, end_state)
	all_move_list += root.next_moves
	while possible_states:
		current_state = possible_states.pop(0)
		if current_state.pegs == end_state:
			get_traversal(current_state)
		else:
			current_state.get_all_valid_moves()
			remove_duplicates(all_move_list, current_state)		
			all_move_list += current_state.next_moves
			for move in current_state.next_moves:
				possible_states.append(game_state(move,current_state))
			possible_states = rank_moves_user_defined(possible_states, end_state)









#Enter the start and end states below. 
#Each inner list represents a peg. Disks are represnted on each of these lists as numbers.
#Please place disks in proper ordering as per the rules of Tower of Hanoi (descending order)
# ex: [[],[],[]] represents 3 pegs
#     [[3,2,1],[],[]] represents 3 pegs with 3 disks on the first peg. 

start_state = [[3,2,1],[],[]]
end_state = [[],[],[3,2,1]]


root = game_state(start_state, [])

print 'Breadth-First-Search:\a'
bfs(root, end_state)

print '\n\n\nDepth-First-Search:'
dfs(root, end_state)

print '\n\n\nBest-First-Search:'
bestfs(root, end_state)

