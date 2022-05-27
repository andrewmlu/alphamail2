from tensorflow import keras
import tensorflow_hub as hub
import tensorflow_text as text

# some inspiration from https://dref360.github.io/keras-web/
class Model:
    def __init__(self):
        self.model = None

    def initialize(self, model):
        self.model = model
        self.model.compile(optimizer='adam', loss='binary_crossentropy')

    def load(self, file_name, file_path='server/model/saved_models'):
        self.model = keras.models.load_model(f'{file_path}/{file_name}',
                                             custom_objects={'KerasLayer': hub.KerasLayer})

    def summary(self):
        return self.model.summary()

    def train(self, train_x, train_y, batch_size=None, epochs=8, val_data=None):
        self.model.fit(train_x, train_y, batch_size=batch_size, epochs=epochs, validation_data=val_data)

    def save(self, file_name, save_format='h5'):
        # prefer h5 format because it is cleaner as a single file
        self.model.save(f'server/model/saved_models/{file_name}', save_format=save_format)

    def evaluate(self, test_x, test_y):
        self.model.evaluate(test_x, test_y)

    def predict(self, predict_x):
        return self.model.predict(predict_x)

