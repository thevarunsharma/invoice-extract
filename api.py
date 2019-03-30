from flask import Flask, request, jsonify, abort
from werkzeug import secure_filename
from rossum.extraction import ElisExtractionApi
import rossum
import pandas as pd
import os

key="areoPIVdQMeDCwrSuKTchVYYSsm3JrLGoJJkJMaYLbdYltarnwx7ZNxfHhMF2kPB"
api = ElisExtractionApi(key)

def get_invoice_details(fname):
    extraction = api.extract(fname)
    df = pd.DataFrame.from_dict(extraction['fields'])
    data = dict(zip(df.title, df.value))
    return data

app = Flask(__name__)

@app.route("/invoice-details/", methods=['POST'])
def main():
    if request.method == 'POST':
        f = request.files.get('file')
        if f is None:
            return "No image uploaded", 400
        fname = secure_filename(f.filename)
        f.save("./images/%s"%fname)
        data = get_invoice_details("./images/%s"%fname)
        os.remove("./images/%s"%fname)
        return jsonify(data)
