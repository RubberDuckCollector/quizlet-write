from pprint import pprint
import random

# Sample dictionary
my_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# Convert dictionary items into a list of tuples
items = list(my_dict.items())

# Shuffle the list of tuples
random.shuffle(items)

# Convert the shuffled list back into a dictionary
shuffled_dict = dict(items)

# Print the shuffled dictionary
print(shuffled_dict)
