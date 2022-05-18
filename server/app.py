from flask import Flask, send_from_directory
from flask_restful import Api, Resource
from apis.retrieval import Retrieval
# from flask_cors import CORS

app = Flask(__name__, static_folder='../client/build', static_url_path='/')
# CORS(app)
api = Api(app)

@app.route('/', defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

api.add_resource(Retrieval, '/retrieval')