from flask import Flask, send_from_directory
from flask_restful import Api, Resource
from apis.retrieval import RetrievalSample, RetrievalStatic
from apis.gmailapi import connect_gmail

# from flask_cors import CORS

connect_gmail()

app = Flask(__name__, static_folder='../client/build', static_url_path='/')
# CORS(app)
api = Api(app)

@app.route('/', defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

api.add_resource(RetrievalStatic, '/retrieval_static')
api.add_resource(RetrievalSample, '/retrieval_sample')

# TODO enable click into emails for reading
# TODO link to database
# TODO importance email ranking