from server.apis.gmailapi import connect_gmail
import server.model.preprocess as preprocess
from server.model.main import Model
import server.model.models as models
from server.model.helpers import save_data

service = connect_gmail()
dataset = preprocess.generate_dataset(service=service, enable_loading=True, file_name='metadata', override=False)
trainX, trainY, valX, valY, testX, testY = preprocess.split_dataset(dataset, 0.6, 0.2, 0.2)

model = Model()
model.load('model_gpt_230418_v1')
print(model.summary())

print('Evaluation:')
predictions, testX_embed, count = model.review(testX, testY, embeddings=True, sort=True, verbose=True)
model.evaluate(testX_embed, testY)

