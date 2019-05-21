import json
from modules import *
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import werkzeug
import sys
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


app = Flask(__name__)
api = Api(app)
CORS(app)
UPLOAD_FOLDER = '../Data/'
cloud_setup()
parser = reqparse.RequestParser()
parser.add_argument(
    'file', type=werkzeug.datastructures.FileStorage, location='files')
port_ = 8080


class Diagnose_(Resource):
    def get(self):
        return cloud_reply()

    def post(self):
        """
        j_response contains list of symptoms
        need to pass json to modules -> Diagnose -> diagnose
        """
        # exit_tf()
        j_response = request.get_json()
        d = Diagnose(j_response)
        # a = []
        # for i in d.diagnosis:
        #     a.append(d.diagnosis[i])
        j_response["diagnosis"] = d.diagnosis
        return j_response


class Train_(Resource):
    def get(self):
        return {"Data Count": len(Data.read_patient_data())}

    def post(self):
        """
        j_response contains list of symptoms and a diagnosis
        need to pass json to modules -> Train -> train

        j_response = request.get_json()
        #j_response = Train.train(j_response)
        return jsonify({"you sent": j_response})
        """
        exit_tf()
        j_response = request.get_json()
        t = Train(j_response)
        j_response = t.prediction
        return j_response


class Select_(Resource):
    def post(self):
        """
        """
        exit_tf()
        j_response = request.get_json()
        t = rand_sug(j_response["disease_name"])
        return t


class Report_(Resource):
    def get(self):
        """
        report_type may be of several kinds
        need to pass report_type to modules -> Data -> generate_report
        """
        return jsonify({"message": "no post"})

    def post(self):
        """
        """
        data = parser.parse_args()
        if data['file'] == "":
            return {"Success": "False"}
        photo = data['file']
        if photo:
            filename = 'a.txt'
            photo.save(os.path.join(UPLOAD_FOLDER, filename))
        return {"Success": "True"}


api.add_resource(Diagnose_, '/diag/')
api.add_resource(Train_, '/train/')
api.add_resource(Report_, '/')
api.add_resource(Select_, '/select/')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', port_))
    app.run(host='0.0.0.0', port=port, threaded=True, debug=False)
