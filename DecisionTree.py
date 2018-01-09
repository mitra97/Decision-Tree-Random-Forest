import csv
import sys
import random

class Tree():
	def __init__(self, key, val=None, children=None):
		self.children = children
		self.key = key ##index number
		self.val = val #if leaf, give class, else it's the attribute value

def build_training_set(file):
	output = {}
	num_attributes = -1
	count = 0
	with open(file, newline='') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			count = count + 1
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
				output.setdefault(key, []).append(index_list)
	return output, num_attributes, count

def build_tree(items_dict, decision_attributes):
	if len(decision_attributes) == 0:
		return Tree(get_most_frequent_classification(items_dict))

	ginis = {}
	for attr in decision_attributes:
		ginis[attr] = gini_index(items_dict, attr)
		if ginis[attr] < 0:
			return Tree(ginis[attr] * -1)
	attribute = min(ginis, key=ginis.get)

	new_attrs = [x for x in decision_attributes if not x == attribute]
	possible_vals = []
	for label, items in items_dict.items():
		possible_vals += [x[attribute - 1] for x in items]
	possible_vals = set(possible_vals)

	children = {}
	for val in possible_vals:
		subset = {}
		for key, items in items_dict.items():
			temp = [x for x in items if x[attribute - 1] == val]
			if len(temp) > 0:
				subset[key] = temp

		if len(subset.keys()) == 0:
			continue

		children[val] = build_tree(subset, new_attrs)

	return Tree(attribute, children=children)

def gini_index(items_dict, attr):
	possible_vals = []
	for label, items in items_dict.items():
			possible_vals += [x[attr - 1] for x in items]
	possible_vals = set(possible_vals)

	total = sum([len(y) for x,y in items_dict.items()])
	counts = {}
	for label, items in items_dict.items():
		if len(items) == total:
			return label * -1
		for val in possible_vals:
			counts.setdefault(val, {})[label] = sum(1 for x in items if x[attr - 1] == val)

	ginis = []
	for val in possible_vals:
		g = 1.0 - sum((x / sum(counts[val].values()))**2
			for x in counts[val].values())
		ginis.append((sum(counts[val].values()) / total) * g)
	return sum(ginis)

def get_most_frequent_classification(items_dict):
	label = -1
	frequency = -1
	for key, val in items_dict.items():
		if len(val) >= frequency:
			frequency = len(val)
			label = key
	return label

def test_tree(root, attributes):
	if not root.children:
		return root.key

	val = attributes[root.key - 1]
	if val in root.children:
		return test_tree(root.children[val], attributes)

	return test_tree(random.choice(list(root.children.values())), attributes)

if __name__ == '__main__':
	items_dict, attrs, count = build_training_set(sys.argv[1])
	attrs = [x+1 for x in list(range(attrs))]
	tree_root = build_tree(items_dict, attrs)

	def print_tree(node, level=0, val=''):
		print('\t'*level + ' ' + str(val) + ': '+ str(node.key))
		if node.children:
			for label, child in node.children.items():
				print_tree(child, level=level+1, val=label)

	test_set, other_attrs, count = build_training_set(sys.argv[2])

	confusion_matrix = []
	for i in range(len(items_dict.keys())):
		confusion_matrix.append([0] * len(items_dict.keys()))

	for label, items in test_set.items():
		for item in items:
			confusion_matrix[label - 1][test_tree(tree_root, item) - 1] += 1

	for i in range(len(confusion_matrix)):
		row = ''
		for j in range(len(confusion_matrix[0])):
			row += '{} '.format(confusion_matrix[i][j])
		print(row)


