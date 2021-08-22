import firebase_admin
import csv
from firebase_admin import credentials, firestore 

cred = credentials.Certificate("./service-account.json")
fbApp = firebase_admin.initialize_app(cred)

db = firestore.client()

with open('operators.csv', 'r', newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for line in csv_reader:
        operator_name = line[0]
        operator_class = line[1]
    
        db.collection("operators").document().set({
            "name": operator_name,
            "class": operator_class
        })
        print(f"Added {operator_name}!")
        
    