"""This is a module "aishvarya.py" and it provides one function called print_lol which print list which may or may not be included in the nested lists. """

def print_lol(the_list, level):
"""This function takes the potential argument called the "the list" which is any of the python list (of, possible nested list). Each data item in the provided list is (recursively)
    printed to the screen on its own time.A second argument called “level" is used to insert tab-stops when a nested list is encountered"""
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item, level)
		else:
			for tab_stop in range(level+1):
				print("\t", end='')
			print(each_item)

