from flask import Flask, request

from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Serve(Resource):
  def get(self):
    return {"message": "no post"}
  
  def post(self):
    j_response = request.get_json()
    return {"you sent": j_response}

class Control(Resource):
  def get(self, num):
    return {"result": num*10}

api.add_resource(Serve, '/')
api.add_resource(Control, '/ctrl/<int:num>')

if __name__ == "__main__":
  app.run(debug=True)