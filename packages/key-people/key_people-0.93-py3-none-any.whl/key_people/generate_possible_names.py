def generate_possible_names(official_name, nicknames):
	ret = []
	for x in nicknames:
		names = official_name.split(" ")
		names = names[1:]
		names = ' '. join(names)
		ret += [x + ' ' + names]

	return ret