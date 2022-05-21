import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Activation, Dropout, Input
from tensorflow.keras.models import load_model, Model
import tensorflow_hub as hub
import tensorflow_text

# install tensorflow-text same version as tensorflow https://www.tensorflow.org/text/guide/tf_text_intro


def model1():
    """
    Based on BERT model as outlined by
    https://www.analyticsvidhya.com/blog/2021/09/performing-email-spam-detection-using-bert-in-python/
    Takes in a string subject line of arbitrary length
    and applies encoding before returning importance score.
    """
    bert_preprocessor = hub.KerasLayer('https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3')
    bert_encoder = hub.KerasLayer('https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4')
    text_input = Input(shape=(), dtype=tf.string)
    preprocessed_text = bert_preprocessor(text_input)
    encoded = bert_encoder(preprocessed_text)
    dropout = Dropout(0.1)(encoded['pooled_output'])
    output = Dense(1, activation='sigmoid')(dropout)

    model = Model(inputs=[text_input], outputs=output)

    return model
