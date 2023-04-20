"""A web application that generates barcodes and stores them in a Google Sheet."""

# pylint: disable=no-member

import random
from flask import Flask, render_template, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1f0g6QFPcuLY-D89Bd-af7nhnJCF1c8AIrcy2vZapAUw'
JSON_KEY_FILE = 'my-service-account-key.json'

creds = service_account.Credentials.from_service_account_file(JSON_KEY_FILE, scopes=SCOPES)
sheets_api = build('sheets', 'v4', credentials=creds)


def get_next_sequence(item_type):
    """Retrieve the next sequence number for the given item_type."""
    sheet_range = 'Sheet1!A:A'
    response = sheets_api.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range=sheet_range).execute()
    values = response.get('values', [])

    max_seq = 0
    for value in values:
        barcode = value[0]
        if barcode[4] == item_type:
            seq = int(barcode[8:12])
            if seq > max_seq:
                max_seq = seq

    return max_seq + 1


def calculate_checksum(barcode):
    """Calculate the checksum for a given barcode."""
    sum_even, sum_odd = 0, 0
    for i, digit in enumerate(barcode[:12]):
        if i % 2 == 0:
            sum_odd += int(digit)
        else:
            sum_even += int(digit)

    sum_total = sum_odd * 3 + sum_even
    return (10 - sum_total % 10) % 10


def generate_barcode(item_type):
    """Generate a barcode for the given item_type."""
    seq = get_next_sequence(item_type)
    seq_str = str(seq).zfill(4)

    barcode = "3" + "".join([str(random.randint(0, 9)) for _ in range(3)])
    barcode += item_type + "".join([str(random.randint(0, 9)) for _ in range(3)]) + seq_str

    checksum = calculate_checksum(barcode)
    return barcode + str(checksum)


@app.route("/")
def index():
    """Render the index page."""
    return render_template("index.html")


@app.route("/generate_barcode", methods=["POST"])
def create_barcode():
    """Generate a new barcode and store it in a Google Sheet."""
    item_type = request.form["item_type"]
    barcode = generate_barcode(item_type)

    sheet_range = 'Sheet1!A:A'
    body = {'values': [[barcode]]}
    sheets_api.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID, range=sheet_range,
        valueInputOption='RAW', insertDataOption='INSERT_ROWS', body=body).execute()

    return jsonify({"barcode": barcode})


# Other imports and Flask app setup...

@app.route('/')
def home():
    return render_template('index.html')

# Other routes and functions...

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
