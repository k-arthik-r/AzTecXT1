from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from configparser import ConfigParser
from datetime import datetime

config = ConfigParser()
config.read('config.ini')

app = Flask(__name__)

client = MongoClient(config['DATABASE']['STRING'])
db = client[config['DATABASE']['DATABASE_NAME']]
collection = db[config['DATABASE']['COLLECTION']]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch')
def fetch():
    return render_template('fetch.html')

@app.route('/savedetails', methods=['POST', 'GET'])
def savedetails():
    appointment_data = request.get_json()

    if not collection.find_one({'_id' : appointment_data['usn']}):

        date = appointment_data['DOB']
        date_object = datetime.strptime(date, '%Y-%m-%d')
        formatted_date = date_object.strftime('%d-%m-%Y')
        id = appointment_data['usn']
        name = appointment_data['name']
        DOB = str(formatted_date)
        address = appointment_data['address']
        blood_group = appointment_data['bloodgroup']
        ph_number = appointment_data['contactnumber']

        data = {
        "_id" : id,
        "name" : name,
        "DOB" : DOB,
        "address" : address,
        "blood_group" : blood_group,
        "ph_number" : ph_number,
        }

        print(data)

        collection.insert_one(data)

        return jsonify(message="Details Saved successfully!")
    
    else:
        date = appointment_data['DOB']
        date_object = datetime.strptime(date, '%Y-%m-%d')
        formatted_date = date_object.strftime('%d-%m-%Y')

        DOB = str(formatted_date)
        address = appointment_data['address']
        blood_group = appointment_data['bloodgroup']
        ph_number = appointment_data['contactnumber']
        name = appointment_data['name']

        query = {'_id' : appointment_data['usn']}
        newquery = {"$set" : {"DOB" : DOB, "address" : address, "blood_group" : blood_group, "ph_number" : ph_number, "name" : name}} 
        collection.update_one(query, newquery)

        return jsonify(message="Data Updated successfully!")
    
@app.route('/fetchdetails', methods=["GET", "POST"])
def fetchdetails():
        usn =" "
        name =" "
        DOB =" "
        address = " "
        blood_group = " "
        message = "Data Not Available"
        ph_number = " "

        if request.method == "POST":
            usnk = request.form["usn"]

            required_one = {
                "_id": usnk,
            }

            data = collection.find_one(required_one)

            if data:
                message = "Data Found!"
                usnf = data["_id"]
                name = data["name"]
                DOB = data["DOB"]
                address = data["address"]
                blood_group = data["blood_group"]
                ph_number = data["ph_number"]

                return render_template("fetch.html", message = message, name = name, usn = usnf, DOB = DOB, address = address, blood_group = blood_group, ph_number = ph_number)

            else:
                return render_template("fetch.html", message = message, name = name, usn = usn, DOB = DOB, address = address, blood_group = blood_group, ph_number = ph_number)


if __name__ == '__main__':
    app.run()
