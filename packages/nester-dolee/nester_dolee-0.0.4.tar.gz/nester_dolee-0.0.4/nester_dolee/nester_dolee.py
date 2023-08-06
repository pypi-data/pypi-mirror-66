""" file(module) comment """

def print_lol(the_list, indent = False ,level=0):
	""" function comment """
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item, indent, level+1)
		else:
			if indent:
				for tab_stop in range(level):
						print("\t", end="")
			print(each_item)


movies = ["The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91, 
			["Graham Chapman",
				["Michael Palin", "John Cleese", "Terry Gilliam", "Eric Idle", "Terry Jones"]]]

names = ['John', 'Eric', ['Cleese', 'Idle'], 'Michael', ['Palin']]