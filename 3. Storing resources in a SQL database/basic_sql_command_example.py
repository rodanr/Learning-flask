import sqlite3

#Establishing the connection with database file or creating
#one if it doesn't exist
connection = sqlite3.connect('data.db')
#creating cursor
cursor = connection.cursor()
#SQL command to create a table with column names id, username, text
create_table = "CREATE TABLE users (id int, username text, password text)"
#Executing the SQL command
cursor.execute(create_table)
#Creating a simple tuple to insert into table
user = (1, 'rodan', 'rodanrjn')
#Inserts ? mark which then replaces by the actual data in line 19
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
#Inserting the user tuple into table
#inserts user into the values replacing the question mark in each column
cursor.execute(insert_query, user)
#list of tuples to insert multiple rows in the table
users = [
	(2, 'rolf', 'asdf'),
	(3, 'anne', 'xyz')
]
#Inserting multiples rows in the column
#Row size increases in each table size increment as the column is always fixed while creating the table
cursor.executemany(insert_query, users)
#Selecting everything from column 
# * can be replaced with column names i.e id, username or password
select_query = "SELECT * FROM users"
#As cursor.execute(select_query) can be iterated by row so doing so
for row in cursor.execute(select_query):
	print(row)
# Commiting all the chages is must
connection.commit()
#Closing the connection with the database file
connection.close()

