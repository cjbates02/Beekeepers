from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os 
import mysql.connector

load_dotenv()

class User:
    def __init__(self, username, unhashed_password):
        self.username = username
        self.password = generate_password_hash(unhashed_password)

    
    def get_database_connection(self):

        user = os.getenv('MYSQL_USER')
        password = os.getenv('MYSQL_PASSWORD') 
        host = os.getenv('MYSQL_HOST')
        database = os.getenv('MYSQL_DATABASE')

        cnx = mysql.connector.connect(user=user, 
                                password=password, 
                                host=host,
                                database=database
                                )
        print("successfully created connection with the database")
        return cnx
    

    def create_user(self):
        cnx = self.get_database_connection()
        cur = cnx.cursor()
        sql =  "INSERT INTO Users (Username, Password) VALUES (%s, %s)"
        val = (self.username, self.password)
        cur.execute(sql, val)
        cnx.commit()
        cur.close()
        cnx.close()


    def delete_user(self, user_id):
        cnx = self.get_database_connection()
        cur = cnx.cursor()
        sql =  f"DELETE FROM Users WHERE Userid={user_id}"
        cur.execute(sql)
        cnx.commit()
        cur.close()
        cnx.close()
 

    def update_username(self):
        cnx = self.get_database_connection()
        cur = cnx.cursor()
        cur.close()
        cnx.close()


    def update_password(self):
        pass


    def validate_credentials(self, username_input, password_input):
        cnx = self.get_database_connection()
        cur = cnx.cursor()
        sql = "SELECT Password FROM Users WHERE Username=%s"
        val = (username_input,)
        cur.execute(sql, val)
        hashed_password = cur.fetchone()
        if not hashed_password:
            print("Could not find username")
            return False
        cur.close()
        cnx.close()
        if check_password_hash(hashed_password[0], password_input):
            print("Successful validation of username and password")
            return True
        print("Password is incorrect")
        return False



if __name__ == '__main__':
    user1 = User('username', 'password')
    user1.create_user()
    #user1.delete_user(1)
    #user1.validate_credentials("username1", "password")
    # user1.validate_credentials("username", "password")
    #user1.validate_credentials("username", "password1")




