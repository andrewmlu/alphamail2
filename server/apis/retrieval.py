from flask_restful import Api, Resource
from server.apis.gmailapi import connect_gmail
from server.apis.helpers import get_ids, get_metadata_from_ids, get_email_from_id

class RetrievalStatic(Resource):
	def get(self):
		return [{'type': 'important', 'id': 5, 'subject': 'hello world', 'author': 'Author 1', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'important', 'id': 6, 'subject': 'bye world', 'author': 'Author 2', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'important', 'id': 7, 'subject': 'hello world', 'author': 'Author 1', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'important', 'id': 8, 'subject': 'bye world', 'author': 'Author 2', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'important', 'id': 9, 'subject': 'bye world', 'author': 'Author 2', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'important', 'id': 10, 'subject': 'bye world', 'author': 'Author 2', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'important', 'id': 1, 'subject': 'hello world', 'author': 'Author 1', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'important', 'id': 2, 'subject': 'bye world', 'author': 'Author 2', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'important', 'id': 3, 'subject': 'bye world', 'author': 'Author 2', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'important', 'id': 4, 'subject': 'hello world', 'author': 'Author 1', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'important', 'id': 11, 'subject': 'bye world', 'author': 'Author 2', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'important', 'id': 12, 'subject': 'bye world', 'author': 'Author 2', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'unimportant', 'id': 65, 'subject': 'hello earth', 'author': 'Author 1', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'unimportant', 'id': 66, 'subject': 'bye earth', 'author': 'Author 2', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'unimportant', 'id': 67, 'subject': 'hello earth', 'author': 'Author 1', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'unimportant', 'id': 68, 'subject': 'bye earth', 'author': 'Author 2', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'unimportant', 'id': 69, 'subject': 'bye earth', 'author': 'Author 2', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'unimportant', 'id': 610, 'subject': 'bye earth', 'author': 'Author 2', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'unimportant', 'id': 61, 'subject': 'hello earth', 'author': 'Author 1', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'unimportant', 'id': 62, 'subject': 'bye earth', 'author': 'Author 2', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'unimportant', 'id': 63, 'subject': 'bye earth', 'author': 'Author 2', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'unimportant', 'id': 64, 'subject': 'hello earth', 'author': 'Author 1', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'unimportant', 'id': 611, 'subject': 'bye earth', 'author': 'Author 2', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'},
		{'type': 'unimportant', 'id': 612, 'subject': 'bye earth', 'author': 'Author 2', 'preview': 'la dee da dee da diddly doo me doo da pa dae doe mi doo'}]

class RetrievalSample(Resource):
	def get(self):
		service = connect_gmail()
		ids = get_ids(service, quantity=25)
		return get_metadata_from_ids(service, ids)

class RetrievalThread(Resource):
	def __init__(self, service):
		self.service = service

	def get(self, id):
		return get_email_from_id(self.service, id)
