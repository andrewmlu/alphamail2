from tensorflow import keras
import tensorflow_hub as hub
import tensorflow_text as text
from server.model.preprocess import get_embeddings

# some inspiration from https://dref360.github.io/keras-web/
class Model:
    def __init__(self):
        self.model = None

    def initialize(self, model, lr=0.001):
        self.model = model
        opt = keras.optimizers.Adam(learning_rate=lr)
        self.model.compile(optimizer=opt, loss='binary_crossentropy')

    def load(self, file_name, file_path='server/model/saved_models'):
        self.model = keras.models.load_model(f'{file_path}/{file_name}',
                                             custom_objects={'KerasLayer': hub.KerasLayer})

    def summary(self):
        return self.model.summary()

    def generate_embeddings(self, x):
        return get_embeddings(x)

    def train(self, train_x, train_y, batch_size=None, epochs=8, val_data=None, embeddings=False):
        if embeddings:
            train_x_embeddings = self.generate_embeddings(train_x)
            if val_data is not None:
                val_x_embeddings, val_y = val_data
                val_x_embeddings = self.generate_embeddings(val_x_embeddings)
                val_data = (val_x_embeddings, val_y)  # sometimes just need to reimport modules when running to debug
            self.model.fit(train_x_embeddings, train_y, batch_size=batch_size, epochs=epochs, validation_data=val_data)
            return train_x_embeddings, val_x_embeddings
        else:
            self.model.fit(train_x, train_y, batch_size=batch_size, epochs=epochs, validation_data=val_data)

    def save(self, file_name, save_format='h5'):
        # prefer h5 format because it is cleaner as a single file
        self.model.save(f'server/model/saved_models/{file_name}', save_format=save_format)

    def evaluate(self, test_x, test_y, embeddings=False):
        if embeddings:
            test_x_embeddings = self.generate_embeddings(test_x)
            self.model.evaluate(test_x_embeddings, test_y)
            return test_x_embeddings
        else:
            self.model.evaluate(test_x, test_y)

    def predict(self, predict_x, embeddings=False):
        if embeddings:
            predict_x_embeddings = self.generate_embeddings(predict_x)
            return self.model.predict(predict_x_embeddings), predict_x_embeddings
        return self.model.predict(predict_x)

    def review(self, predict_x, y_true=None, embeddings=False, sort=False, verbose=False):
        if embeddings:
            predict_x_embeddings = self.generate_embeddings(predict_x)
            predict_y = self.model.predict(predict_x_embeddings)
        else:
            predict_y = self.model.predict(predict_x)
        if sort:
            predict_y, predict_x, y_true = zip(*sorted(zip(predict_y, predict_x, y_true), reverse=True))
        if verbose:
            count = [0]
            for i, prediction in enumerate(predict_y):
                if y_true is not None:
                    print(predict_x[i], prediction, y_true[i])
                else:
                    print(predict_x[i], prediction)
                if y_true[i] == 1:
                    count.append(count[-1]+1)
                else:
                    count.append(count[-1])
        if embeddings:
            return predict_y, predict_x_embeddings, count
        else:
            return predict_y, count