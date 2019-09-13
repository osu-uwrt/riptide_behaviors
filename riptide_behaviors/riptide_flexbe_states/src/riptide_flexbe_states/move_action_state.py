#!/usr/bin/env python
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyActionClient

# example import of required action
#move action and goal should be here
from chores.msg import DoDishesAction, DoDishesGoal


class MoveActionState(EventState):
	'''
	Actionlib actions are the most common basis for state implementations
	since they provide a non-blocking, high-level interface for robot capabilities.
	The example is based on the DoDishes-example of actionlib (see http://wiki.ros.org/actionlib).
	This time we have input and output keys in order to specify the goal and possibly further evaluate the result in a later state.


	'''

	def __init__(self):
		# See example_state.py for basic explanations.
		super(MoveActionState, self).__init__(outcomes = ['success', 'failed', 'command_error']
												 )

		

		# Create the action client when building the behavior.
		# This will cause the behavior to wait for the client before starting execution
		# and will trigger a timeout error if it is not available.
		# Using the proxy client provides asynchronous access to the result and status
		# and makes sure only one client is used, no matter how often this state is used in a behavior.
		self._topic = 'do_dishes'
		self._client = ProxyActionClient({self._topic: DoDishesAction}) # pass required clients as dict (topic: type)

		# It may happen that the action client fails to send the action goal.
		self._error = False


	def execute(self, userdata):
		# While this state is active, check if the action has been finished and evaluate the result.

		# Check if the client failed to send the goal.
		if self._error:
			return 'command_error'

		# Check if the action has been finished
		if self._client.has_result(self._topic):
			result = self._client.get_result(self._topic)
			

			# In this example, we also provide the amount of cleaned dishes as output key.
			

			# Based on the result, decide which outcome to trigger.
			

		# If the action has not yet finished, no outcome will be returned and the state stays active.
		

	def on_enter(self, userdata):
		# When entering this state, we send the action goal once to let the robot start its work.

		# As documented above, we get the specification of which dishwasher to use as input key.
		# This enables a previous state to make this decision during runtime and provide the ID as its own output key.
		
		# Create the goal.
		

		# Send the goal.
		self._error = False # make sure to reset the error state since a previous state execution might have failed
		try:
			self._client.send_goal(self._topic, goal)
		except Exception as e:
			# Since a state failure not necessarily causes a behavior failure, it is recommended to only print warnings, not errors.
			# Using a linebreak before appending the error log enables the operator to collapse details in the GUI.
			Logger.logwarn('Failed to send the move command:\n%s' % str(e))
			self._error = True


	def on_exit(self, userdata):
		# Make sure that the action is not running when leaving this state.
		# A situation where the action would still be active is for example when the operator manually triggers an outcome.

		if not self._client.has_result(self._topic):
			self._client.cancel(self._topic)
			Logger.loginfo('Cancelled active action goal.')
		
