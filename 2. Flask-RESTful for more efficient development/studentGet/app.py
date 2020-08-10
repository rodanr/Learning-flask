from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

#Defining resource
class Student(Resource):
    #Defining methods this resource is gonna accept like post,get etc for now only implementing get
    def get(self, name):
        return {'student':name}
    
    

api.add_resource(Student, '/student/<string:name>') #http://127.0.0.1:5000/student/Rodan

app.run(port=5000)