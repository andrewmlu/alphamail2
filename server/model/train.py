from server.apis.gmailapi import connect_gmail
import server.model.preprocess as preprocess
from server.model.main import Model
import server.model.models as models
from server.model.helpers import save_data, load_data

service = connect_gmail()
dataset = preprocess.generate_dataset(service=service, enable_loading=True, file_name='metadata', override=False)
trainX, trainY, valX, valY, testX, testY = preprocess.split_dataset(dataset, 0.6, 0.2, 0.2)

model = Model()
model.initialize(models.model5())
model.summary()

print(len(trainX))

# train from scratch
# trainX_embed, valX_embed = model.train(trainX, trainY, epochs=100, val_data=(valX, valY), embeddings=True)
# save_data(trainX_embed, 'trainX_embed')
# save_data(valX_embed, 'valX_embed')

# train from scratch no embeddings
model.train(trainX, trainY, epochs=100, val_data=(valX, valY), embeddings=False)

# train from saved embeddings
# trainX_embed, valX_embed = load_data('server/data/trainX_embed'), load_data('server/data/valX_embed')
# model.train(trainX_embed, trainY, epochs=100, val_data=(valX_embed, valY), embeddings=False)

model.save('model_bert2_230422_1')

print('Evaluation:')
# evaluate from saved embeddings
# predictions, testX_embed, count = model.review(testX, testY, embeddings=True, sort=True, verbose=True)
# model.evaluate(testX_embed, testY)

# evaluate from scratch no embeddings
model.review(testX, testY, embeddings=False, sort=True, verbose=True)
model.evaluate(testX, testY)

