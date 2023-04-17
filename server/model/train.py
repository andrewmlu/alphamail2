from server.apis.gmailapi import connect_gmail
import server.model.preprocess as preprocess
from server.model.main import Model
import server.model.models as models
from server.model.helpers import save_data

service = connect_gmail()
dataset = preprocess.generate_dataset(service=service, file_name='dataset_230416')
trainX, trainY, valX, valY, testX, testY = preprocess.split_dataset(dataset, 0.6, 0.2, 0.2)

model = Model()
model.initialize(models.model3())
print(model.summary())

trainX_embed, valX_embed = model.train(trainX, trainY, epochs=100, val_data=(valX, valY), embeddings=True)
save_data(trainX_embed, 'trainX_embed')
save_data(valX_embed, 'valX_embed')
model.save('model_gpt_230416_1')

print('Evaluation:')
predictions, testX_embed, count = model.review(testX, testY, embeddings=True, sort=True, verbose=True)
model.evaluate(testX_embed, testY)

