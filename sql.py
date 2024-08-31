import sqlite3

try:
    connection = sqlite3.connect("database.db")

    cursor = connection.cursor()
    try:
        table1_info = """
        Create table USERS(USER_ID INT,SURVEY_ID INT);
        """
        cursor.execute(table1_info)
        cursor.execute('''Insert Into USERS values(1,101)''')
        cursor.execute('''Insert Into USERS values(2,101)''')
        cursor.execute('''Insert Into USERS values(3,102)''')
        cursor.execute('''Insert Into USERS values(4,102)''')
        cursor.execute('''Insert Into USERS values(5,103)''')
        print("USERS Table Created.")
    except sqlite3.Error as e:
        print(f"Error creating or inserting into USERS table: {e}")

    try:
        table2_info = """
        Create table SURVEY(SURVEY_ID INT,QUESTION_ID INT, QUESTION VARHCAR(25));
        """
        cursor.execute(table2_info)
        cursor.execute('''Insert Into SURVEY values(101,1,'How satisfied are you with our service?')''')
        cursor.execute('''Insert Into SURVEY values(101,2,'Would you recommend our service to others?')''')
        cursor.execute('''Insert Into SURVEY values(102,3,'How easy was it to use the product?')''')
        cursor.execute('''Insert Into SURVEY values(102,4,'How likely are you to use the product again?')''')
        print("SURVEY Table Created.")
    except sqlite3.Error as e:
        print(f"Error creating or inserting into SURVEY table: {e}")

    try:
        table3_info = """
        Create table RESPONSES(USER_ID INT,SURVEY_ID INT,QUESTION_ID INT,RESPONSE VARCHAR(25));
        """
        cursor.execute(table3_info)
        cursor.execute('''Insert Into RESPONSES values(1,101,1,'Very satisfied')''')
        cursor.execute('''Insert Into RESPONSES values(1,101,2,'Yes')''')
        cursor.execute('''Insert Into RESPONSES values(2,101,1,'Satisfied')''')
        cursor.execute('''Insert Into RESPONSES values(2,101,2,'Maybe')''')
        cursor.execute('''Insert Into RESPONSES values(3,102,3,'Easy')''')
        cursor.execute('''Insert Into RESPONSES values(3,102,4,'Very likely')''')
        cursor.execute('''Insert Into RESPONSES values(4,102,3,'Difficult')''')
        cursor.execute('''Insert Into RESPONSES values(4,102,4,'Unlikely')''')
        cursor.execute('''Insert Into RESPONSES values(5,103,1,'Neutral')''')
        print("RESPONSES Table Created.")
    except sqlite3.Error as e:
        print(f"Error creating or inserting into RESPONSES table: {e}")

    connection.commit()
except sqlite3.Error as e:
    print(f"Database error: {e}")

finally:
    if connection:
        connection.close()
        print("Database connection closed.")