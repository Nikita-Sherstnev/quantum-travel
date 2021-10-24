from flask import Flask
from flask_restful import Resource, Api

from api import graph
from flask_cors import CORS

app = Flask(__name__, static_folder='../client/dist/',    static_url_path='/')
CORS(app)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return app.send_static_file('index.html')

api.add_resource(HelloWorld, '/')
api.add_resource(graph.Graph, '/graph')

if __name__ == '__main__':
    app.run(debug=True)