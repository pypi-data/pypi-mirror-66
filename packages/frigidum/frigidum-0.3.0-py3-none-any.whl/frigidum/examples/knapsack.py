"""
	Knapsack Problem

	Problem Instance: ks_10000_0

	Exercise from Knapsack from
	Professor Pascal Van Hentenryck's discrete optimization course 
	https://coursera.org/course/optimization

	Best Known Bag Value: 1099893

	Note: As this is a maximization we simple make the objective
	negative

"""
import os
import re
import frigidum

import numpy as np


"""
	Loading the data
"""

FRIGIDUM_PATH = os.path.dirname( frigidum.__file__ )
DATA_PATH = FRIGIDUM_PATH + '/data_files/'

ks_10000_0_path = DATA_PATH + 'ks_10000_0'

np_values = None
np_weights = None

knapsack_capacity = 0

greedeness_power = 5

"""
	Read & Parse the data
"""
with open(ks_10000_0_path) as f:
	lines = f.read().split('\n')

	first_line = lines[0].split()
	items = int(first_line[0])
	capacity = int(first_line[1])

	values = []
	weights = []

	for i in range(1, items+1):
		line = lines[i]
		parts = line.split()

		values.append(int(parts[0]))
		weights.append(int(parts[1]))

	np_values = np.array(values)
	np_weights = np.array(weights)
	knapsack_capacity = capacity


relative_value = np_values / np_weights

"""
	Explode/power the relative weights.

	This specific problem has lots of relative values
	close to each other, which requires a high
	explodation.

	For more scattered items, a softer
	power factor should be chosen.
"""

relative_value = relative_value ** 150


def random_knapsack():
	"""
		Random Bag - Randomly picks items untill full, without being smart
	"""
	random_order = np.random.permutation( np.arange(np_weights.size) )
	random_order_inverse = np.argsort( random_order )
	random_indices = np.cumsum(np_weights[random_order]) < knapsack_capacity
	indices = random_indices[random_order_inverse]
	return indices

def reconsider_few_items( bag ):
	return reconsider_items_poisson_based( bag, ratio=.05 )

def reconsider_many_items( bag ):
	return reconsider_items_poisson_based( bag, ratio=.3 )

def reconsider_items_poisson_based( bag, ratio=.5 ):
	new_bag = bag.copy()
	items_in_bag = np.sum( bag )
	

	"""
		We use the Poisson Distribution to select the number of items
		to reconsider.

		We use relative value to prioritize not so value items
	"""
	items_to_reconsider = 1 + np.random.poisson( np.ceil(items_in_bag * ratio) )
	
	items_to_reconsider = np.min( [ np.sum(bag), items_to_reconsider] )

	items_drop_value = np.max(relative_value[bag]) - relative_value[bag] + .1
	items_drop_value = items_drop_value / np.max(items_drop_value)
	drop_steepness = 1 + np.random.poisson(greedeness_power)
	items_drop_value = items_drop_value ** drop_steepness
	drop_weights = 	items_drop_value / np.sum(items_drop_value)

	items_to_drop = np.random.choice( np.argwhere(bag).flatten() , items_to_reconsider, replace=False, p=drop_weights)
	
	new_bag[ items_to_drop ] = False

	items_out_of_bag = np.argwhere(~bag).flatten()

	"""
		More steep, will prioritize items with large
		relative value.

		Too steep have risk being stuck in local minima.
	"""
	relative_value_steepness = 1 + np.random.poisson(greedeness_power)

	none_zero_relative_value = 0.1 + relative_value[~bag]
	maxone_relative_weights = none_zero_relative_value / np.max(none_zero_relative_value)
	steep_relative_weights = maxone_relative_weights ** relative_value_steepness
	norm_relative_weights = steep_relative_weights / np.sum(steep_relative_weights)

	"""
		Items with high relative value have more chance to be picked.
		This phenomenon is being exxagerated by using the power, relative_value_steepness.

		When relative_value_steepness is large, it is almost greedy.
		When relative_value_steepness is small, seemingly 
		uninteresting items are also chosen (small relative value).

	"""
	new_potential_items = np.random.choice( np.argwhere(~bag).flatten() , np.sum(~bag), replace=False, p=norm_relative_weights)

	space_left_in_bag = knapsack_capacity - np.sum( np_weights[new_bag] )

	new_items_that_fit = np.cumsum(np_weights[new_potential_items]) < space_left_in_bag
	new_items_indicis = new_potential_items[new_items_that_fit]

	new_bag[new_items_indicis] = True

	"""
		It might be, that the bag still has space, lets fill!
	"""
	if np.all(new_items_that_fit):
		none_zero_relative_value = 0.1 + relative_value[~new_bag]
		maxone_relative_weights = none_zero_relative_value / np.max(none_zero_relative_value)
		steep_relative_weights = maxone_relative_weights ** relative_value_steepness
		norm_relative_weights = steep_relative_weights / np.sum(steep_relative_weights)

		new_potential_items = np.random.choice( np.argwhere(~new_bag).flatten() , np.sum(~new_bag), replace=False, p=norm_relative_weights)
		space_left_in_bag = knapsack_capacity - np.sum( np_weights[new_bag] )

		new_items_that_fit = np.cumsum(np_weights[new_potential_items]) < space_left_in_bag
		new_items_indicis = new_potential_items[new_items_that_fit]
		new_bag[new_items_indicis] = True

	return new_bag


def objective_function(bag):
	return -np.sum( np_values[bag] )

