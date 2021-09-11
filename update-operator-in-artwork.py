import firebase_admin
import csv
from firebase_admin import credentials, firestore


if __name__ == "__main__":
    name = "main"

    cred = credentials.Certificate("./service-account.json")
    firebase_app = firebase_admin.initialize_app(cred)

    db = firestore.client()

    artworks_collection_ref = db.collection("projects").document(
        "main").collection("artworks")
    artwork_array = []

    artwork_db = artworks_collection_ref.stream()

    for artwork in artwork_db:
        artwork_dict = artwork.to_dict()
        artwork_dict["uid"] = artwork.id
        artwork_array.append(artwork_dict)

    operators_array = []

    operators_db = db.collection("operators").stream()

    failed_to_write = []

    for operator in operators_db:
        operator_dict = operator.to_dict()
        operator_dict["uid"] = operator.id
        operators_array.append(operator_dict)

    for art in artwork_array:
        artwork_uid = art["uid"]
        operator_uid = art["operator"]["uid"]

        print(artwork_uid, operator_uid)
        operator = list(
            filter(lambda op: op["uid"] == operator_uid, operators_array))

        if(len(operator) != 1):
            failed_to_write.append(art)
            print(f"Failed to update {art['operator']['name']}")
        else:
            artworks_collection_ref.document(artwork_uid).update(
                {f"operator": operator[0]})
            print(f"Updated artwork {artwork_uid} with operator!")

    print("Failed to update the following:")
    print(failed_to_write)
