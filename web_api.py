from flask import Flask, request
from flask_restful import Resource, Api
from flask_oauthlib.provider import OAuth2Provider
from modules import *
import json

app = Flask(__name__)
api = Api(app)


class Diagnose(Resource):
  def get(self):
    return {"message": "no post"}
  
  def post(self):
    """
    j_response contains list of symptoms
    need to pass json to modules -> Diagnose -> diagnose
    """
    j_response = request.get_json()
    j_response = Diagnose.diagnose(j_response)
    return {"Diagnosed Symptom": j_response}


class Train(Resource):
  def get(self):
    return {"message": "no post"}
  
  def post(self):
    """
    j_response contains list of symptoms and a diagnosis
    need to pass json to modules -> Train -> train
    """
    j_response = request.get_json()
    return {"you sent": j_response}


class Report(Resource):
  def get(self, report_type):
    """
    report_type may be of several kinds
    need to pass report_type to modules -> Data -> generate_report
    """
    return {"message": "no post"}


api.add_resource(Diagnose, '/diag/')
api.add_resource(Train, '/train/')
api.add_resource(Report, '/data/')

if __name__ == "__main__":
  app.run(debug=True)
