from database_management import open_connection, find_ticker, commit_close
import pkg_resources

NICKNAME_FILE = pkg_resources.resource_filename('ticker_to_searchable_terms', 'DB/Stocks.db')
conn, c = open_connection(NICKNAME_FILE)
c = c.execute('select * from Stocks')
names = list(map(lambda x: x[0], c.description))
print(names)

command =			'''ALTER TABLE Stocks
									ADD alt_company_name text'''

#c.execute(command)




corp_names = ['inc', 'corp', 'ltd', 'lp', 'fund']
command = '''UPDATE Stocks
			SET alt_company_name = Replace(name, '', '')
			'''
c.execute(command)

command = '''UPDATE Stocks
			SET alt_company_name = Replace(alt_company_name, '{}', '')
			'''

for x in corp_names:
	ex_com = command.format(' ' + x + '.')
	c.execute(ex_com)
	ex_com = command.format(' ' + x.capitalize() + '.')
	c.execute(ex_com)
	ex_com = command.format(x)
	c.execute(ex_com)
	ex_com = command.format(' ' + x.capitalize())
	c.execute(ex_com)


ret = find_ticker("MSFT", c)
commit_close(conn)
print(ret)