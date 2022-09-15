import psycopg2



# hostname = 'localhost'
#         port='5432'
#         username = 'postgres'
#         password = 'admin'
#         database = 'demo'
#Establishing the connection
conn = psycopg2.connect(
   database="demo", user='postgres', password='admin', host='127.0.0.1', port= '5432'
)
#Setting auto commit false
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

# Preparing SQL queries to INSERT a record into the database.
cursor.execute('''INSERT INTO test.itviec(
	 company_name, day_work, country, no_employee, job_title, job_skill, job_description)
	VALUES ( 'AAA', 'monday-friday', 'Viet Nam', 100, 'Software Engineer', 'Python', 'No description')''')
# cursor.execute('''INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX,
#    INCOME) VALUES ('Vinay', 'Battacharya', 20, 'M', 6000)''')
# cursor.execute('''INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX,
#    INCOME) VALUES ('Sharukh', 'Sheik', 25, 'M', 8300)''')
# cursor.execute('''INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX,
#    INCOME) VALUES ('Sarmista', 'Sharma', 26, 'F', 10000)''')
# cursor.execute('''INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX,
#    INCOME) VALUES ('Tripthi', 'Mishra', 24, 'F', 6000)''')

# Commit your changes in the database
conn.commit()
print("Records inserted........")

# Closing the connection
conn.close()