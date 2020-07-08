#####################################################################
##  Interfaces that must be implemented by the client

#####
# WorldState -- all information needed to check for goal and to generate 
#    successor states
#
#  Method successors() must return a tuple:  (worldState, action)
#    -- the data type of action is up to the client
# 
# * Implementation must be aware that it is going to be stored and compared
#      against other states:  override hash and equals appropriately
# * Implementation must not share state across instances!

class WorldState:
	def successors():
		raise "Not implemented"
		
#############################################
# Problem -- must supply the initial state and a goal state checker   
	
class Problem:
	# Method initial returns a world state
	def initial(self):
		raise "Not implemented"
		
	# Method isGoal returns a boolean
	def isGoal(self, state):
		raise "Not implemented"

#############################################
# Evaluator
#    Client provides g(s) and h*(s) in the form of actionsCoster and goalEstimator      
#    Evaluator superclass provides the evaluator f(s) = g(s) + h*(s)
#
#  Note: unlike WorldState and Problem, Evaluator is not an abstract class;
#    clients will instantiate Evaluator directly

class Evaluator:
	def __init__(self, actionsCoster, goalEstimator):
		self._estimator = goalEstimator
		self._coster = actionsCoster
	def estimateToGoal(self, state):
		return self._estimator(state)
	def costSoFar(self, actions):
		return self._coster(actions)
	def value(self, state, actions):
		return self.estimateToGoal(state) + self.costSoFar(actions)