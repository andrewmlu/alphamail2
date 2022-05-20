from flask import Flask, send_from_directory
from flask_restful import Api, Resource
from apis.retrieval import RetrievalSample, RetrievalStatic, RetrievalThread
from apis.gmailapi import connect_gmail

# from flask_cors import CORS

service = connect_gmail()

app = Flask(__name__, static_folder='../client/build', static_url_path='/')
# CORS(app)
api = Api(app)

@app.route('/', defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

# TODO understand why the api.add_resource links don't go to 404 not found
@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')

api.add_resource(RetrievalStatic, '/api/retrieval_static')
api.add_resource(RetrievalSample, '/api/retrieval_sample')
api.add_resource(RetrievalThread, '/api/thread/<id>', resource_class_kwargs={'service': service})

# TODO enable click into emails for reading
# TODO link to database
# TODO importance email ranking