from .database_management import find_ticker, open_connection, find_nicknames
def remove_initial(inp):
	names = inp.split(" ")
	ret = []
	for x in names.split(" "):
		if len(x) <= 1:
			ret.append(x)
		elif x[1] != '.':
			ret.append(x)

	ret = ' '.join(ret)

	return ret

def generate_possible_names(official_name, c):
	ret = []

	nicknames = find_nicknames(official_name.split(" ")[0], c)
	official_name = remove_initial(official_name)
	if nicknames == None:
		return [official_name]


	for x in nicknames:
		names = official_name.split(" ")
		names = names[1:]
		names = ' '. join(names)
		x = x.capitalize()
		ret += [x + ' ' + names]

	return ret


def gen_names(ticker, c):
	results = find_ticker(ticker, c)
	people = []
	conn, c = open_connection("DB/Nicknames.db")
	for x in results[2:-1]:
			if x != 'NULL':
				find_nicknames
				x = generate_possible_names(x, c)
				people.append(x)
	return people

