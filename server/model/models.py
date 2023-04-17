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
    # DONE 2022.05.21-01.39 include trainable parameters
    # DONE 2022.05.21-01.39 try different encoder layers
    text_input = Input(shape=(), dtype=tf.string)
    preprocessed_text = bert_preprocessor(text_input)
    encoded = bert_encoder(preprocessed_text)
    dropout = Dropout(0.1)(encoded['pooled_output'])
    output = Dense(1, activation='sigmoid')(dropout)

    model = Model(inputs=[text_input], outputs=output)

    return model


def model2():
    """
    This BERT model modifies the previous one in two ways.
    First, it utilizes a smaller model, with 10 hidden layers for the encoder, as opposed to 12,
    and a hidden size of 256 rather than 768. Second, it fine-tunes all parameters and makes
    the encoding layer trainable.
    """
    bert_preprocessor = hub.KerasLayer('https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3')
    bert_encoder = hub.KerasLayer('https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-128_A-2/2')

    text_input = Input(shape=(), dtype=tf.string)

    preprocessed_text = bert_preprocessor(text_input)
    encoded = bert_encoder(preprocessed_text)
    dropout = Dropout(0.2)(encoded['pooled_output'])
    output = Dense(1, activation='sigmoid')(dropout)

    model = Model(inputs=[text_input], outputs=output)

    return model


def model3():
    """
    GPT-3 based embeddings model for email classification
    """
    input = Input(shape=(1536,))
    dropout = Dropout(0.05)(input)
    output = Dense(1, activation='sigmoid')(dropout)
    model = Model(inputs=[input], outputs=output)

    return model
