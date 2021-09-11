import firebase_admin
import csv
from firebase_admin import credentials, firestore


if __name__ == "__main__":
    name = "main"

    cred = credentials.Certificate("./service-account.json")
    firebase_app = firebase_admin.initialize_app(cred)

    db = firestore.client()

    artists_db = db.collection("artists").stream()

    artists_array = []

    for artist in artists_db:
        artist_dict = artist.to_dict()
        artist_dict["uid"] = artist.id
        artists_array.append(artist_dict)

    operators_array = []

    operators_db = db.collection("operators").stream()

    for operator in operators_db:
        operator_dict = operator.to_dict()
        operator_dict["uid"] = operator.id
        operators_array.append(operator_dict)

    failed_to_update = []

    with open('operator-rarity.csv', 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for line in csv_reader:
            op_name = line[1]
            rarity = int(line[0].replace("*", ""))

            print(op_name, rarity)

            operator = list(
                filter(lambda op: op["name"] == op_name, operators_array))

            print(operator)
            if(len(operator) != 1):
                failed_to_update.append(op_name)
                print("Failed to update, adding to logs")
            else:
                target_operator = operator[0]  # the operator we want to update

                operator_id = target_operator["uid"]
                print(operator_id)

                operator_ref = db.collection("operators").document(operator_id)
                operator_ref.update({u"rarity": rarity})
                print(f"successfully updated ${op_name}")

    print("Failed to update the following:")
    print(failed_to_update)
