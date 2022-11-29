import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
from Environment import *
from Parameters import *

def create_q_model():
    # Network defined by the Deepmind paper
    inputs = layers.Input(shape=(16,1))

    layer1 = layers.Dense(512, activation="relu")(inputs)
    action = layers.Dense(num_actions, activation="linear")(layer1)

    return keras.Model(inputs=inputs, outputs=action)
