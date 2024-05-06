from flask import Flask, jsonify, request;
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from bson import json_util
import json
import os


load_dotenv()

app = Flask(__name__)

client = MongoClient("", server_api=ServerApi('1'))
db = client["vihari"]
CORS(app)

@app.route('/createZone', methods=["POST"])
def zone():
    incoming_msg = request.get_json();
    zone = db['Zone']
    admin = db["Admins"]
    driver = list(db["Driver"].find({"firstname": "Driver" }))
    zone_admin = admin.find_one({"firstname": "Bamsi"})
    zone_dict = {
        "zone_name": incoming_msg['zoneName'],
        "added_by": "Admin",
        "geofence_radius": '',
        "price_matrix": [],
        "total_vehicles": [],
        "total_drivers": driver,
        "status": ""
    }

    zone.insert_one(zone_dict)
    # print(driver)
    # print(driver.find())
    
    return "working...."


@app.route('/getZones')
def getzones():
    zones = db['Zone']
    
    zone = zones.find()
    zone_list = list(zone)
    # for items in zone:
    #     zone_dict = {
    #         "zone_name": items["zone_name"],
    #         "geofence_radius": items["geofence_radius"],
    #         "price_matrix": items["price_matrix"],
    #         "total_vehicles": items["total_vehicles"],
    #         "total_drivers": items["total_drivers"]
    #     }
    # zone_list.append(zone_dict)
    
    
    return json.loads(json_util.dumps(zone_list))


@app.route('/getVendors')
def getvendors():
    vendors = db['Vendors']
    
    vendor = vendors.find()
    vendor_list = list(vendor)
    # for items in zone:
    #     zone_dict = {
    #         "zone_name": items["zone_name"],
    #         "geofence_radius": items["geofence_radius"],
    #         "price_matrix": items["price_matrix"],
    #         "total_vehicles": items["total_vehicles"],
    #         "total_drivers": items["total_drivers"]
    #     }
    # zone_list.append(zone_dict)
    
    
    return json.loads(json_util.dumps(vendor_list))

@app.route('/getDrivers')
def getDrivers():
    drivers = db['Driver']
    
    driver = drivers.find()
    driver_list = list(driver)
    # for items in zone:
    #     zone_dict = {
    #         "zone_name": items["zone_name"],
    #         "geofence_radius": items["geofence_radius"],
    #         "price_matrix": items["price_matrix"],
    #         "total_vehicles": items["total_vehicles"],
    #         "total_drivers": items["total_drivers"]
    #     }
    # zone_list.append(zone_dict)
    
    
    return json.loads(json_util.dumps(driver_list))

@app.route('/createDriver', methods=["POST"])
def createDriver():
    incoming_msg = request.get_json()["Body"];
    drivers = db["Driver"]
    zone = db["Zone"]
    zone = db["Zone"].find_one({"zone_name": incoming_msg["zone"]})
    driver_dict = {
        "firstname": incoming_msg["firstName"],
        "lastname": incoming_msg["lastName"],
        "mobile": incoming_msg["mobile"],
        "alt_mobile": incoming_msg["altNumber"],
        "email": incoming_msg["email"],
        "zone": zone,
        "license_number":incoming_msg["licenseNumber"],
        "driving_license":incoming_msg["drivingPhoto"],
        "id_proof_front_url": incoming_msg["imgUrl"],
        "address_proof_url": incoming_msg["addressProof"],
        "pan_card": incoming_msg["pan"],
        "calender_availability": ""
    }
    drivers.insert_one(driver_dict)

    return "working..."

@app.route('/createAdmin')
def createAdmin():
    # incoming_msg = request.get_json();
    
    admin = db['Admins']
    zones = db["Zone"]
    zoneAdmin = zones.find_one({"zone_admin.name": "Bamsi"})
    admin_dict = {
        "firstname": "Bamsi",
        "lastName": "c",
        "contact": "+917981395086",
        "email": "hh989940@gmail.com",
        "license_number": "",
        "role": 'admin'
    }
    admin.insert_one(admin_dict)
    # print(zoneAdmin)
    return "working..."


@app.route('/createCustomer', methods=["POST"])
def createCustomer():
    incoming_msg = request.get_json()
    customer = db['Customer']
    email = customer.find_one({"email": incoming_msg['email']})
    if (email):
        return "already used that email"

    else:
        customer_dict = {
            "firstname": incoming_msg['firstName'],
            "lastname": incoming_msg['lastName'],
            "mobile": incoming_msg["phoneNumber"],
            "email": incoming_msg['email'],
            "location": {
                "lat": '',
                "long": ''
            },
            "search_history": [],
            "booking_history": [],
            "total_payments": "",
            "pending_payments": "",
            "feedback": [],
            "status": "",
            "profile_url": "",
            'role': "user"
        }

        customer.insert_one(customer_dict)
        
    # print(incoming_msg)
    return "working...."

@app.route('/checkCustomer', methods=["POST"])
def checkCustomer():
    incoming_msg = request.get_json()
    customers = db['Customer']
    admin = db['Admins']
    zoneAdmin = db['ZoneAdmins']
    vendor = db['Vendors']
    customer = customers.find_one({"mobile": incoming_msg["phoneNumber"]})
    onlyAdmin = admin.find_one({"contact": incoming_msg['phoneNumber']})
    onlyZoneAdmin = zoneAdmin.find_one({"mobile": incoming_msg['phoneNumber']})
    onlyVendors = vendor.find_one({"mobile": incoming_msg['phoneNumber']})


    if customer:
        return json.loads(json_util.dumps(customer))
    elif onlyAdmin:
        return json.loads(json_util.dumps(onlyAdmin))
    elif onlyZoneAdmin:
        return json.loads(json_util.dumps(onlyZoneAdmin))
    elif onlyVendors:
        return json.loads(json_util.dumps(onlyVendors))
    else:
        return "You are not registered, please register first", 400





@app.route('/createVendor', methods=["POST"])
def createVendor():
    incoming_msg = request.get_json()["Body"];
    vendors = db['Vendors']
    zone = db["Zone"].find_one({"zone_name": incoming_msg["zone"]})
    vendors_dict = {
        "zone_id": zone['_id'],
        "firstname": incoming_msg["firstName"],
        "lastname": incoming_msg["lastName"],
        "mobile": incoming_msg["mobile"],
        "alt_mobile": incoming_msg["altNumber"],
        "email": incoming_msg["email"],
        "zone": zone,
        "license_number": incoming_msg["licenseNumber"],
        "driving_license_front_url": incoming_msg["drivingPhoto"],
        "driving_license_back_url": "",
        "address_proof_url": incoming_msg["imgUrl"],
        "id_proof_front_url" :"",
        "id_proof_back_url": "",
        "profile_url": incoming_msg["profilePic"],
        "pan_card": "",
        "role": "vendor"
        
    }

    vendors.insert_one(vendors_dict)
    # print(incoming_msg)
    return "working....."

@app.route('/createZoneAdmin', methods=["POST"])
def createZoneAdmin():
    incoming_msg = request.get_json()["Body"];
    zone_admins = db['ZoneAdmins']
    zone = db["Zone"].find_one({"zone_name": incoming_msg["zone"]})
    vendors_dict = {
        "zone_id": zone['_id'],
        "firstname": incoming_msg["firstName"],
        "lastname": incoming_msg["lastName"],
        "mobile": incoming_msg["mobile"],
        "alt_mobile": incoming_msg["altNumber"],
        "email": incoming_msg["email"],
        "zone": zone,
        "license_number": incoming_msg["licenseNumber"],
        "driving_license_front_url": incoming_msg["drivingPhoto"],
        "driving_license_back_url": "",
        "address_proof_url": incoming_msg["imgUrl"],
        "id_proof_front_url" :"",
        "id_proof_back_url": "",
        "profile_url": incoming_msg["profilePic"],
        "pan_card": "",
        "role": "zoneAdmin"
        
    }

    zone_admins.insert_one(vendors_dict)
    # print(incoming_msg)
    return "working....."

@app.route('/createVehicle', methods=["POST"])
def createVehicle():
    incoming_msg = request.get_json()["Body"];
    zone_admins = db['Vehicles']
    zone = db["Zone"].find_one({"zone_name": incoming_msg["zone"]})
    driver = db['Driver'].find_one({"firstname": incoming_msg["driverId"]})
    vehicle_dict = {
        "zone_id": zone['_id'],
        "vehicle_name": incoming_msg["vehicleName"],
        "vehicle_model": incoming_msg["vehicleModel"],
        "vehicle_type": incoming_msg["vehicleType"],
        "brand": incoming_msg["brand"],
        "capacity": incoming_msg["capacity"],
        "zone": zone,
        "mileage": incoming_msg["mileage"],
        "vehicle_owner": incoming_msg["ownerType"],
        "cost_per_hour": incoming_msg["costPerHour"],
        "driver_id": driver['_id'],
        "added_by" :incoming_msg["addedBy"],
        "vehicle_calender_availability": "",
        "status": "",
        "rc_certificate": incoming_msg['rcCertificateUrl'],
        "premit_certificate": incoming_msg["permitCertificateUrl"],
        "fitness_certificate": incoming_msg["fitnessCertificateUrl"],
        "insurance_certificate": incoming_msg["insuranceCertificateUrl"],
        "pollution_certificate": incoming_msg["pollutionCertificateUrl"]
        
    }

    zone_admins.insert_one(vehicle_dict)
    # print(driver['_id'])
    return "working....."

if __name__ == '__main__':
    app.run()