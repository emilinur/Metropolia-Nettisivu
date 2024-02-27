from flask import Flask
from flask import request
from flask import jsonify
import json
import mysql.connector
from flask import render_template

app = Flask(__name__)

# Replace these values with your database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'metropolia_nettisivu'
}

class User:
    def __init__(self, username=None, password=None, email=None, courses=None, user_type=None) -> None:
        self.username = username
        self.password = password
        self.email = email
        self.courses = courses
        self.user_type = user_type
    
    def get(self):
        conn = mysql.connector.connect(**db_config)

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Insert the user into the 'users' table
        insert_query = "SELECT * FROM users WHERE email=%s;"
        user_data = (self.email)

        try:
            user_result = cursor.fetchone(insert_query, user_data)
            conn.commit()
            cursor.close()
            conn.close()
            
            if user_result:
                # Process the user data
                user_id = user_result[0]
                username = user_result[1]
                user_email = user_result[3]
                password = user_result[2]
                user_courses = user_courses[4]
                user_type = user_result[5]
                return {"message":"Here is the user","user":{"id":f"{user_id}","username":f"{username}", "password":f"{password}","email":f"{user_email}","type":f"{user_type}"}}
            else:
                return {"message": "error retrieving user"}
        except mysql.connector.Error as err:
            raise TypeError("Error saving user to DB")
        
    def login(self):
        conn = mysql.connector.connect(**db_config)

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Insert the user into the 'users' table
        insert_query = "SELECT * FROM users WHERE email=%s and password=%s;"
        user_data = (self.email, self.password)

        try:
            user_result = cursor.fetchone(insert_query, user_data)
            conn.commit()
            cursor.close()
            conn.close()
            
            if user_result:
                # Process the user data
                user_id = user_result[0]
                username = user_result[1]
                password = user_result[2]
                user_email = user_result[3]
                user_type = user_result[4]
                return {"message":"Here is the user","user":{"id":f"{user_id}","username":f"{username}", "password":f"{password}","email":f"{user_email}","type":f"{user_type}"}}
            else:
                raise TypeError("error retrieving user")
        except mysql.connector.Error as err:
            raise TypeError("Error saving user to DB")  

    def create(self):
        # ESTABLISH CONNECTION TO DATABASE
        # Create a connection to the database
        conn = mysql.connector.connect(**db_config)

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Insert the user into the 'users' table
        insert_query = "INSERT INTO users (username, password, email, user_type) VALUES (%s, %s, %s)"
        user_data = (self.username, self.password, self.email, self.user_type)

        try:
            cursor.execute(insert_query, user_data)
            conn.commit()
            cursor.close()
            conn.close()
            return {"message": "User inserted successfully"}
        except mysql.connector.Error as err:
            raise TypeError("Error saving user to DB")
        
    def enroll(self, newCourse):
        # ESTABLISH CONNECTION TO DATABASE
        # Create a connection to the database
        conn = mysql.connector.connect(**db_config)

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Insert the user into the 'users' table
        update_query = "UPDATE users SET couses=CONCAT(courses, %s) WHERE email=%s"
        user_data = (newCourse, self.email)

        try:
            cursor.execute(update_query, user_data)
            conn.commit()
            cursor.close()
            conn.close()
            return {"message": "Course added successfully"}
        except mysql.connector.Error as err:
            raise TypeError("Error connecting to DB")
    
    def delete(self):
        # ESTABLISH CONNECTION TO DATABASE
        # Create a connection to the database
        conn = mysql.connector.connect(**db_config)

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Delete the user from the 'users' table
        delete_query = "DELETE FROM users WHERE username = %s"
        user_data = self.username

        try:
            cursor.execute(delete_query, user_data)
            conn.commit()
            cursor.close()
            conn.close()
            return {"message": "User deleted successfully"}
        except mysql.connector.Error as err:
            raise TypeError("Error deleting user from DB")

class Course:
    def __init__(self, name=None, credits=None, teacherEmail=None) -> None:
        self.name = name
        self.credits = credits
        self.teacherEmail = teacherEmail
    
    def getAll(self):
        conn = mysql.connector.connect(**db_config)

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Insert the user into the 'users' table
        fetch_query = "SELECT * FROM courses;"

        try:
            cursor.execute(fetch_query)
            courses_result = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
            
            if courses_result:
                # Process the user data
                rs = json.dumps(dict(courses_result))
                return {"message":"Here are the courses","courses":rs}
            else:
                return {"message": "error retrieving courses"}
        except mysql.connector.Error as err:
            raise TypeError("Error connecting to DB")
        
    def create(self)->None:
        # ESTABLISH CONNECTION TO DATABASE
        # Create a connection to the database
        conn = mysql.connector.connect(**db_config)

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Insert the user into the 'users' table
        insert_query = "INSERT INTO courses (name, credits, teacherEmail) VALUES (%s, %s, %s)"
        course_data = (self.name, self.credits, self.teacherEmail)

        try:
            cursor.execute(insert_query, course_data)
            conn.commit()
            cursor.close()
            conn.close()
            return {"message": "Course created successfully"}
        except mysql.connector.Error as err:
            raise TypeError("Error saving course to DB")

@app.route("/getUser", methods = ["GET"])
def getUser():
    json_data = request.json
    
    if not json_data:
        return jsonify({"error": "Invalid JSON data"}), 400

    # Get user details from the JSON data
    email = json_data.get('email') # email = "user123@gmail.com"
    
    user = User(email)

    try:
        response = user.get()
        return jsonify(response)
    except TypeError as err:
        return jsonify('{"error":"error happened processing your request"}')

@app.route("/createUser", methods = ["POST"])
def createCourse():
    # Get JSON data from the request
    json_data = request.json

    # REQUEST VALIDATION, if not JSON been sent, return 400
    if not json_data:
        return jsonify({"error": "Invalid JSON data"}), 400

    # Get user details from the JSON data
    username = json_data.get('username') # username = "user123"
    password = json_data.get('password') # password = "password123"
    email = json_data.get('email') # email = "at@at.com"
    user_type = json_data.get('user_type') # user_type = "student"

    user = User(username, password, email, user_type)

    try:
        response = user.create()
        return jsonify(response)
    except TypeError as err:
        return jsonify('{"error":"error happened processing your request"}')
    
@app.route("/createcourse", methods = ["POST"])
def createCourse():
    # Get JSON data from the request
    json_data = request.json

    # REQUEST VALIDATION, if not JSON been sent, return 400
    if not json_data:
        return jsonify({"error": "Invalid JSON data"}), 400

    # Get user details from the JSON data
    name = json_data.get('name') # name = "course123"
    credits = json_data.get('credits') # credits = "5"
    teacherEmail = json_data.get('teacherEmail') # teacherEmail = "t@t.t"

    course = Course(name, credits, teacherEmail)

    try:
        response = course.create()
        return jsonify(response)
    except TypeError as err:
        return jsonify('{"error":"error happened processing your request"}')

@app.route("/deleteUser", methods = ["DELETE"])
def deleteCourse():
    # Get JSON data from the request
    json_data = request.json

    # REQUEST VALIDATION, if not JSON been sent, return 400
    if not json_data:
        return jsonify({"error": "Invalid JSON data"}), 400

    # Get user details from the JSON data
    username = json_data.get('username') # username = "user123"
    password = json_data.get('password') # password = "password123"
    user_type = json_data.get('user_type') # user_type = "student"

    user = User(username, password, user_type)

    try:
        response = user.delete()
        return jsonify(response)
    except TypeError as err:
        return jsonify('{"error":"error happened processing your request"}')

class Kurssi:
    def __init__(self, nimi: str, op: int):
        self.nimi = nimi
        self.op = op
    def __repr__(self):
        return f"{self.nimi}({self.op}op)"
    def __eq__(self, other):
        return self.nimi == other.nimi and self.op == other.op
    
class Opintosuoritus:
    def __init__(self, kurssi: Kurssi, arvosana: int):
        self.kurssi = kurssi
        self.arvosana = arvosana
    def __repr__(self):
        return f"{self.kurssi}: {self.arvosana}"
    
class Tarjotin:
    def __init__(self, nimi: str):
        self.nimi = nimi
        self.kurssit = []
    def __repr__(self):
        return f"{self.nimi}: {self.kurssit}"
    def lisaa(self, kurssi: Kurssi):
        if not kurssi in self.kurssit:
            self.kurssit.append(kurssi)

class Opiskelija:
    def __init__(self, nimi: str, tarjotin: Tarjotin):
        self.nimi = nimi
        self.tarjotin = tarjotin
        self.suoritukset = []
        self.aktiiviset = []
    def __repr__(self):
        return f"{self.nimi}({self.tarjotin.nimi}) {self.suoritukset} - {self.aktiiviset}"
    def ilmoittaudu(self, kurssi: Kurssi):
        if (not kurssi in [suoritus.kurssi for suoritus in self.suoritukset] 
            and kurssi in self.tarjotin.kurssit 
            and not kurssi in self.aktiiviset):
            self.aktiiviset.append(kurssi)
    def suorita(self, kurssi: Kurssi, arvosana: int):
        if kurssi in self.aktiiviset:
            suoritus = Opintosuoritus(kurssi, arvosana)
            self.suoritukset.append(suoritus)
            self.aktiiviset.remove(kurssi)
    def opintopisteet(self):
        yht = 0
        for suoritus in self.suoritukset:
            yht += suoritus.kurssi.op
        return yht
    def opintopisteet1(self):
        return sum([s.kurssi.op for s in self.suoritukset])
    def painotettuKA(self):
        if self.suoritukset == []:
            return 0
        else:
            return sum([s.kurssi.op*s.arvosana for s in self.suoritukset]) / sum([s.kurssi.op for s in self.suoritukset])

#Opettajan luokka, jossa opettajalle annetaan hlo kohtanen ID, nimi, lisataan ja poistetaan kursseja ja listataan sen opettamat kurssit.
class Opettaja: #Emilia
    opettaja_maara = 0 

    def __init__(self, nimi: str):
        Opettaja.opettaja_maara += 1
        self.opettajaID = Opettaja.opettaja_maara
        self.nimi = nimi
        self.opettajan_kurssit = []

    def __repr__(self):
        return f"Opettaja ID: {self.opettajaID}, Nimi: {self.nimi}, Opettajan kurssit: {self.opettajan_kurssit}"

    def lisaa_kurssi(self, kurssi: Kurssi):
        if kurssi not in self.opettajan_kurssit:
            self.opettajan_kurssit.append(kurssi)

    def poista_kurssi(self, kurssi: Kurssi):
        if kurssi in self.opettajan_kurssit:
            self.opettajan_kurssit.remove(kurssi)

    def opettajan_kurssit(self):
        return self.opettajan_kurssit



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test")
def home1():
    return render_template("register.html")