from flask import Flask, request
from flask_restful import Resource, Api
from flask_oauthlib.provider import OAuth2Provider
from flask import jsonify
import sys, os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from modules import *
import json

app = Flask(__name__)
api = Api(app)


class Diagnose_(Resource):
  def get(self):
    Data.prepare_keys()
    ls_ = [[i.lower(), Data.symptom_name_to_id[i]] for i in Data.symptom_name_to_id.keys()]
    ret = []
    for i in sorted(sorted(ls_)):
      j = {}
      k, l = i
      j["name"] = k
      j["id"] = l
      ret.append(j)
    return jsonify(ret)
  
  def post(self):
    """
    j_response contains list of symptoms
    need to pass json to modules -> Diagnose -> diagnose
    """
    j_response = request.get_json()
    j_response = Diagnose.diagnose(j_response)
    return jsonify({"Diagnosed Symptom": j_response})


class Train_(Resource):
  def get(self):
    return {"message": "no post"}
  
  def post(self):
    """
    j_response contains list of symptoms and a diagnosis
    need to pass json to modules -> Train -> train
    
    j_response = request.get_json()
    #j_response = Train.train(j_response)
    return jsonify({"you sent": j_response})
    """
    j_response = request.get_json()
    j_response = Diagnose.diagnose(j_response)
    return jsonify({"Diagnosed Symptom": j_response})


class Report_(Resource):
  def get(self, report_type):
    """
    report_type may be of several kinds
    need to pass report_type to modules -> Data -> generate_report
    """
    return jsonify({"message": "no post"})


api.add_resource(Diagnose_, '/diag/')
api.add_resource(Train_, '/train/')
api.add_resource(Report_, '/data/')

if __name__ == "__main__":
  app.run(host='0.0.0.0', threaded=True, debug=True)
