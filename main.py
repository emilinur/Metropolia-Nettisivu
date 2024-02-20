from flask import Flask
from flask import request
from flask import jsonify
import mysql.connector

app = Flask(__name__)

# Replace these values with your database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'metropolia_nettisivu'
}

class User:
    def __init__(self, username=None, password=None, email=None, user_type=None):
        self.username = username
        self.password = password
        self.email = email
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
                password = user_result[2]
                user_email = user_result[3]
                user_type = user_result[4]
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

#Anastasiia
class Opo:
	
	def jatkoopinto(self, opintopisteet: opintopisteet):
		if opintopisteet>=60:
			return True
		else:
			return False

#Testaus 

#Kurssit
matematiikka = Kurssi("Matematiikka", 5)
fysiikka = Kurssi("Fysiikka", 5)
englanti = Kurssi("Englanti", 10)

#kurssi tarjottimen luominen --> opon homma
tarjotin = Tarjotin("Tarjotin")
tarjotin.lisaa(matematiikka)
tarjotin.lisaa(fysiikka)
tarjotin.lisaa(englanti)

#Luodaan opiskelijat ja opettajat
opiskelija = Opiskelija("Matti", tarjotin)

opettaja1 = Opettaja("Pekka")
opettaja2 = Opettaja("Milla")

#Opiskelija class metodin testaus
opiskelija.ilmoittaudu(matematiikka)
opiskelija.ilmoittaudu(fysiikka)
opiskelija.suorita(matematiikka, 4)
opiskelija.suorita(fysiikka, 5)
print(opiskelija)

#Opettaja class metodin testaus
opettaja1.lisaa_kurssi(matematiikka)
opettaja1.lisaa_kurssi(fysiikka)
opettaja2.lisaa_kurssi(englanti)
print(opettaja1)
print(opettaja2)
print("Opettajan kurssit:", opettaja1.opettajan_kurssit)
print("Opettajan kurssit:", opettaja2.opettajan_kurssit)