import sqlite3

def create_table(c, table_name, cols, types):

	command = 'CREATE TABLE '
	command += table_name
	command += ' ('
	if (len(cols) != len(types) and len(types) != 1):
		raise Exception("len cols must be equal to len types")

	if len(types) == 1:
		types = types * len(cols)

	for x in range(len(cols)):
		if x != 0:
			command += ", "
		command += cols[x]
		command += " "
		command += types[x]
	command += ")"
	c.execute(command)

def find_ticker(ticker, c):
	ticker = [ticker]
	c.execute('SELECT * FROM stocks WHERE symbol=?', ticker)
	return c.fetchone()

def find_nicknames(name, c):
	name = [name.lower()]
	c.execute('SELECT * FROM nicknames WHERE name=?', name)
	prefilter = c.fetchone()
	if prefilter == None:
		return prefilter
	ret = []
	for x in prefilter:
		if x != 'NULL':
			ret.append(x)
	return ret


"""UPDATE dbo.xxx
SET Value = REPLACE(Value, '123\', '')
WHERE ID <=4"""

def add_ticker(entry, c):
	c.execute('INSERT INTO stocks VALUES (?,?,?,?,?,?,?,?)', entry)

def add_nicknames(entries, c):
	c.executemany('INSERT INTO nicknames VALUES (?,?,?,?,?)', entries)

def add_many_entry(entries, c):
	c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?,?,?,?)', entries)

def open_connection(file):
	conn = sqlite3.connect(file)
	c = conn.cursor()
	return conn, c

def commit_close(conn):
	conn.commit()
	conn.close()