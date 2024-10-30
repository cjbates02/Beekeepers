from dotenv import load_dotenv
import os 
import mysql.connector

load_dotenv()

user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD') 
host = os.getenv('MYSQL_HOST')
database = os.getenv('MYSQL_DATABASE')

print(user, password, host, database)

cnx = mysql.connector.connect(user=user, 
                              password=password, 
                              host=host
                             )


cnx.close()


