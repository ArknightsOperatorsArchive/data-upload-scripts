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

    failed_to_write = []

    with open('assignments.csv', 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for line in csv_reader:
            artist_display_name, operator = line[1], line[0]

            print(f"Searching for {artist_display_name} who drew {operator}")

            # Find target artist in artists_dict using display_name
            artist = list(filter(
                lambda artist: artist["displayName"] == artist_display_name, artists_array))

            # Find target operator in operators_array using name
            operator = list(
                filter(lambda op: op["name"] == operator, operators_array))

            # We make sure that there's only 1 artist and operator returned
            if(len(artist) != 1 or len(operator) != 1):
                failed_to_write.append({
                    "artist": artist_display_name,
                    "operator": operator
                })
                print("Failed to write, adding to logs")
            else:
                artwork_dict = {
                    "artist": dict(artist[0]),
                    "operator": dict(operator[0]),
                    "status": "Assigned"
                }
                print(artwork_dict)
                ref = db.collection("projects").document(
                    "main").collection("artworks").document()
                ref.set(artwork_dict)
                print(f"Added artwork {artwork_dict} assigned to {artist}!")

    print("Failed to write the following:")
    print(failed_to_write)
