import sys
import random
import csv
from DecisionTree import build_tree, test_tree, build_training_set

def build_random_set(file, num_items):
	item_list = []
	num_attributes = -1
	count = 0
	with open(file, newline='') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			for val in row:
				ptInfo = val.split(' ')
				index_list = []
				key = int(ptInfo[0])
				for i in range(len(ptInfo)):
					if i != 0:
						words = ptInfo[i]
						words = words.split(":")
						index_list.append(int(words[1]))
				num_attributes = max(num_attributes, len(index_list))
				item_list.append((key, index_list))

	output = {}
	for i in range(num_items):
		key, val = random.choice(item_list)
		output.setdefault(key, []).append(val)

	return output, num_attributes
num_trees = 0
tree_size = 0
file_type = sys.argv[2]

if file_type == 'balanced.scale.test':
	num_trees = 700
	tree_size = 200
elif file_type == 'led.test':
	num_trees = 300
	tree_size = 200
elif file_type == 'nursery.test':
	num_trees = 250
	tree_size = 200
elif file_type == "synthetic_social.test":
	num_trees = 300
	tree_size = 250
else:
	num_trees = 300
	tree_size = 250


forest = []
for i in range(num_trees):
	items_dict, attrs = build_random_set(sys.argv[1], tree_size)
	attrs = [x+1 for x in list(range(attrs))]	
	forest.append(build_tree(items_dict, attrs))

test_set = build_training_set(sys.argv[2])[0]
items_dict, attrs, count = build_training_set(sys.argv[1])
confusion_matrix = []
for i in range(len(items_dict.keys())):
	confusion_matrix.append([0] * len(items_dict.keys()))

for label, items in test_set.items():
	for item in items:
		votes = {}
		for tree in forest:
			vote = test_tree(tree, item)
			votes[vote] = votes.setdefault(vote, 0) + 1
		winner = max(votes, key=votes.get)
		confusion_matrix[label - 1][winner - 1] += 1

for i in range(len(confusion_matrix)):
	row = ''
	for j in range(len(confusion_matrix[0])):
		row += '{} '.format(confusion_matrix[i][j])
	print(row)