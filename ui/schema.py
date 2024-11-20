from dotenv import load_dotenv
import os 
import mysql.connector

load_dotenv()

#cnx.close()


def get_database_connection():

    user = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD') 
    host = os.getenv('MYSQL_HOST')
    database = os.getenv('MYSQL_DATABASE')

    cnx = mysql.connector.connect(user=user, 
                              password=password, 
                              host=host,
                              database='user_pass'
                             )
    print("successfully created connection with the database")
    return cnx


if __name__ == '__main__':
    cnx = get_database_connection()
    cur = cnx.cursor()
    # cur.execute('''
    #     CREATE TABLE users (
    #         user_id INT PRIMARY KEY,
    #         username VARCHAR(20),
    #         password VARCHAR(20)
    # )
    # ''')
    # cur.close()
    # cur = cnx.cursor()
    sql =  "INSERT INTO users (user_id, username, password) VALUES (%s, %s, %s)"
    val = (0, 'drewromesser', 'password1234')
    val = (1, 'noname', 'nopassword')
    cur.execute(sql, val)
    cnx.commit()
    cur.close()
    cur = cnx.cursor()
    #cur.execute('USE user_pass;')
    cur.execute("SELECT * FROM users")
    result = cur.fetchall()
    print(result)
    cur.close()
