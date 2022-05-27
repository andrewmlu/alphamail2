from server.apis.gmailapi import connect_gmail
import server.model.preprocess as preprocess
from server.model.main import Model
import server.model.models as models

service = connect_gmail()
dataset = preprocess.generate_dataset(service=service)
trainX, trainY, valX, valY, testX, testY = \
    preprocess.split_dataset(dataset, 0.6, 0.2, 0.2)

model = Model()
model.initialize(models.model1())
print(model.summary())

model.train(trainX, trainY, epochs=6, val_data=(valX, valY))
model.save('model_bert0522_1')

print('Evaluation:')
model.evaluate(testX, testY)