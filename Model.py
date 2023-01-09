import numpy as np
import tensorflow as tf
import datetime
from tensorflow import keras
from keras import layers
from Environment import *
from Parameters import *

def create_q_model():
    # Network defined by the Deepmind paper
    inputs = layers.Input(16*16)

    layer1 = layers.Dense(512, activation="relu")(inputs)
    layer2 = layers.Dense(256, activation="relu")(layer1)
    action = layers.Dense(4, activation="softmax")(layer2)

    return keras.Model(inputs=inputs, outputs=action, )

def save_model(model,path=model_save_path):
    model.save(path+str(datetime.datetime.now()))

def load_model(path=default_model):
    return keras.models.load_model(path)