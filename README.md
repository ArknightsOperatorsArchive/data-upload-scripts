# Bulk Upload Scripts

These are a set of scripts used to upload operator, and artwork data to the firestore database for the AoA website

## Development

To develop you will need

- pip3
- python3

You will also need a service account file from Firebase, rename this file to `service-account.json` and put it into the root directory of this module

### Install Preqs

To install prerequisites, run using a terminal

```sh
$ pip3 install -r requirements.txt
```

## Data Files

Artists should be already in the database, under the "artists" collection

- assignments.csv: should have 2 columns with no header: Operator Name, Artist
- operators.csv: should have 2 columns with no header: Operator Name, Operator Class

This will intiailize the project with projectId `main` with artworks under the "Assigned" status

### LICENSE

This repo is licensed under `MIT` see (./LICENSE)[LICENSE] for more details
