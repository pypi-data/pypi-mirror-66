""" file(module) comment """
def print_lol(the_list):
	""" function comment """
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item)
		else:
			print(each_time)

